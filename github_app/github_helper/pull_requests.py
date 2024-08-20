import requests
import logging
import os
from github_app.github_helper.utils import get_diff_text, get_pr_files
from github_app.github_helper.installation import get_installation_access_token
from github_app.github_helper.permissions import PULL_REQUEST_PERMISSION
from kaizen.reviewer.code_review import CodeReviewer
from kaizen.generator.pr_description import PRDescriptionGenerator
from kaizen.formatters.code_review_formatter import create_pr_review_text
from kaizen.llms.provider import LLMProvider

logger = logging.getLogger(__name__)

GITHUB_API_BASE_URL = os.environ["GITHUB_API_BASE_URL"]

ACTIONS_TO_PROCESS_PR = ["opened", "reopened", "review_requested", "ready_for_review"]
ACTIONS_TO_UPDATE_DESC = ["opened", "reopened"]


confidence_mapping = {
    "critical": 5,
    "important": 4,
    "moderate": 3,
    "low": 2,
    "trivial": 1,
}


def process_pull_request(payload):
    comment_url = payload["pull_request"]["comments_url"]
    repo_name = payload["repository"]["full_name"]
    pull_number = payload["pull_request"]["number"]
    diff_url = GITHUB_API_BASE_URL + f"/repos/{repo_name}/pulls/{pull_number}.diff"
    review_url = GITHUB_API_BASE_URL + f"/repos/{repo_name}/pulls/{pull_number}/reviews"
    pr_files_url = GITHUB_API_BASE_URL + f"/repos/{repo_name}/pulls/{pull_number}/files"
    installation_id = payload["installation"]["id"]
    pr_title = payload["pull_request"]["title"]
    pr_description = payload["pull_request"]["body"]

    access_token = get_installation_access_token(
        installation_id, PULL_REQUEST_PERMISSION
    )

    diff_text = get_diff_text(diff_url, access_token)

    # Get PR Files
    pr_files = get_pr_files(pr_files_url, access_token)

    reviewer = CodeReviewer(llm_provider=LLMProvider(default_temperature=0.1))
    review_data = reviewer.review_pull_request(
        diff_text=diff_text,
        pull_request_title=pr_title,
        pull_request_desc=pr_description,
        pull_request_files=pr_files,
        user=repo_name,
    )
    if repo_name == "Cloud-Code-AI":
        tests = generate_tests(pr_files)
    topics = clean_keys(review_data.topics, "important")
    review_desc = create_pr_review_text(topics)
    comments, topics = create_review_comments(topics)

    post_pull_request(comment_url, review_desc, installation_id, tests=tests)
    for review in comments:
        post_pull_request_comments(review_url, review, installation_id)

    return True, review_desc.decode("utf-8")


def create_review_comments(topics, confidence_level=4):
    # Store confidence level in Config
    comments = []
    for _, reviews in topics.items():
        for review in reviews:
            if confidence_mapping[review["confidence"]] > confidence_level:
                comments.append(review)
    return comments, topics


def process_pr_desc(payload):
    pr_url = payload["pull_request"]["url"]
    repo_name = payload["repository"]["full_name"]
    pull_number = payload["pull_request"]["number"]
    diff_url = GITHUB_API_BASE_URL + f"/repos/{repo_name}/pulls/{pull_number}.diff"
    pr_files_url = GITHUB_API_BASE_URL + f"/repos/{repo_name}/pulls/{pull_number}/files"
    installation_id = payload["installation"]["id"]
    pr_title = payload["pull_request"]["title"]
    pr_description = payload["pull_request"]["body"]

    access_token = get_installation_access_token(
        installation_id, PULL_REQUEST_PERMISSION
    )

    pr_files = get_pr_files(pr_files_url, installation_id)
    sorted_files = sort_files(pr_files)

    diff_text = get_diff_text(diff_url, access_token)
    desc_generator = PRDescriptionGenerator(llm_provider=LLMProvider())
    description = desc_generator.generate_pull_request_desc(
        diff_text=diff_text,
        pull_request_title=pr_title,
        pull_request_desc=pr_description,
        pull_request_files=sorted_files,
        user=repo_name,
    )
    patch_pr_body(pr_url, description.desc, installation_id)


def post_pull_request(url, data, installation_id, tests=None):
    access_token = get_installation_access_token(
        installation_id, PULL_REQUEST_PERMISSION
    )
    data = {
        "body": f"{data}\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️"
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.post(url, headers=headers, json=data)
    logger.debug(f"Post Pull request response: {response.text}")


def patch_pr_body(url, data, installation_id):
    access_token = get_installation_access_token(
        installation_id, PULL_REQUEST_PERMISSION
    )
    data = {"body": data}
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.patch(url, headers=headers, json=data)
    logger.debug(f"Patch Pull request response: {response.text}")


def clean_keys(topics, min_confidence=None):
    ## Remove this after kaizen fix
    if min_confidence:
        try:
            min_value = confidence_mapping[min_confidence]
        except Exception:
            print("Error")
    else:
        min_value = float("-inf")  # Include all items if no min_confidence is given

    new_topics = {}
    issues = []
    for topic, reviews in topics.items():
        rev = []
        for review in reviews:
            if not review.get("reasoning"):
                review["reasoning"] = review["comment"]
            if confidence_mapping[review["confidence"]] >= min_value:
                issues = review
                rev.append(review)

        new_topics[topic] = rev
    print("issues: ", issues)
    return new_topics


def post_pull_request_comments(url, review, installation_id):
    access_token = get_installation_access_token(
        installation_id, PULL_REQUEST_PERMISSION
    )
    data = {
        "event": "REQUEST_CHANGES",
        "comments": [
            {
                "path": review["file_name"],
                "start_line": review["start_line"],
                "line": review["end_line"],
                "body": review["comment"],
            }
        ],
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.post(url, headers=headers, json=data)
    logger.debug(f"Post Review comment response: {response.text}")


def sort_files(files):
    sorted_files = []
    for file in files:
        min_index = len(sorted_files)
        file_name = file["filename"]
        for i, sorted_file in enumerate(sorted_files):
            if file_name < sorted_file["filename"]:
                min_index = i
                break
        sorted_files.insert(min_index, file)
    return sorted_files


def generate_tests(pr_files):
    return [f["filename"] for f in pr_files]
