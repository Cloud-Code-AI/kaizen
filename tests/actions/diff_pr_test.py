import requests
from kaizen.reviewer.code_review import CodeReviewer
from kaizen.llms.provider import LLMProvider
import json
from kaizen.formatters.code_review_formatter import create_pr_review_text
from github_app.github_helper.pull_requests import clean_keys, create_review_comments
from kaizen.generator.pr_description import PRDescriptionGenerator

# GitHub API endpoint
GITHUB_API = "https://api.github.com"

headers = {
    "Accept": "application/vnd.github.v3+json",
}


def get_pr_info(owner, repo, pr_number):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_pr_files(owner, repo, pr_number):
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/files"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_diff(url):
    headers = {
        "Accept": "application/vnd.github.v3.diff",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = requests.get(url, headers=headers)
    return response.text


def main(owner, repo, pr_number):
    try:
        pr_info = get_pr_info(owner, repo, pr_number)
        pr_files = get_pr_files(owner, repo, pr_number)
        print(f"\nDiff URL: {pr_info['diff_url']}")
        diff_text = get_diff(pr_info["diff_url"])
        print(f"Diff: \n{diff_text}\n")
        code_reviewer = CodeReviewer(llm_provider=LLMProvider())
        reviews = code_reviewer.review_pull_request(
            pull_request_title=pr_info["title"],
            pull_request_desc=pr_info["body"],
            diff_text=diff_text,
            pull_request_files=pr_files,
            user="local_test",
        )
        print(json.dumps(reviews.topics, indent=2))

        print("Processing Reviews ....")
        topics = clean_keys(reviews.topics, "moderate")
        review_desc = create_pr_review_text(topics)
        comments, topics = create_review_comments(topics)

        print(f"\n Review Desc: \n {review_desc}")

        print(f"\nComments: \n{json.dumps(comments)}")

        print("################### CODE DESC")
        desc_generator = PRDescriptionGenerator(llm_provider=LLMProvider())
        description = desc_generator.generate_pull_request_desc(
            pull_request_title=pr_info["title"],
            pull_request_desc=pr_info["body"],
            diff_text=diff_text,
            pull_request_files=pr_files,
            user="local_test",
        )

        print("Description: \n", description.desc)

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main("Cloud-Code-AI", "kaizen", 252)

    print("------------------- Multi File -------------------")
    main("Cloud-Code-AI", "kaizen", 222)
