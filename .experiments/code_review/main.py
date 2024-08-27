import os
import json
import datetime
import logging
from tqdm import tqdm
from kaizen.reviewer.code_review import CodeReviewer
from kaizen.llms.provider import LLMProvider
from github_app.github_helper.utils import get_diff_text, get_pr_files
from github_app.github_helper.pull_requests import (
    create_review_comments,
)
from kaizen.formatters.code_review_formatter import create_pr_review_text

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Set up logging
log_file = os.path.join(SCRIPT_DIR, "pr_review.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def process_pr(pr_url, reeval_response=False):
    logger.info(f"Processing PR: {pr_url}")
    pr_diff = f"{pr_url}.patch"
    pr_files = f"{pr_url}/files".replace("github.com", "api.github.com/repos").replace(
        "/pull", "/pulls"
    )
    pr_title = pr_url.split("/")[-1]  # Use PR number as title for simplicity

    diff_text = get_diff_text(pr_diff, "")
    pr_files = get_pr_files(pr_files, "")

    reviewer = CodeReviewer(llm_provider=LLMProvider(), default_model="best")
    review_data = reviewer.review_pull_request(
        diff_text=diff_text,
        pull_request_title=pr_title,
        pull_request_desc="",
        pull_request_files=pr_files,
        user="kaizen/example",
        reeval_response=reeval_response,
        model="best",
    )

    # topics = clean_keys(review_data.topics, "important")
    logger.info(review_data.topics)
    review_desc = create_pr_review_text(
        review_data.issues, code_quality=review_data.code_quality
    )
    review_desc = f"PR URL: {pr_url}\n\n" + review_desc
    review_desc += f"\n\n----- Cost Usage ({review_data.model_name})\n" + json.dumps(
        review_data.usage
    )
    comments, topics = create_review_comments(review_data.topics)
    logger.info(f"Model: {review_data.model_name}\nUsage: {review_data.usage}")
    logger.info(f"Completed processing PR: {pr_url}")
    return review_desc, comments, review_data.issues


def save_review(pr_number, review_desc, comments, issues, folder):
    folder = os.path.join(folder, f"pr_{pr_number}")
    logger.info(f"Saving review for PR {pr_number} in {folder}")
    os.makedirs(folder, exist_ok=True)
    review_file = os.path.join(folder, "review.md")
    comments_file = os.path.join(folder, "comments.json")
    issues_file = os.path.join(folder, "issues.json")

    with open(review_file, "w") as f:
        f.write(review_desc)

    with open(comments_file, "w") as f:
        json.dump(comments, f, indent=2)

    with open(issues_file, "w") as f:
        json.dump(issues, f, indent=2)

    logger.info(f"Saved review files for PR {pr_number}")


def main(pr_urls):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base_folder = os.path.join(SCRIPT_DIR, f"code_reviews_{timestamp}")
    with_eval_folder = os.path.join(base_folder, "with_eval")
    no_eval_folder = os.path.join(base_folder, "no_eval")

    os.makedirs(with_eval_folder, exist_ok=True)
    os.makedirs(no_eval_folder, exist_ok=True)

    logger.info(f"Created output folders: {base_folder}")

    for pr_url in tqdm(pr_urls, desc="Processing PRs", unit="PR"):
        pr_number = pr_url.split("/")[-1]

        logger.info(f"Starting to process PR {pr_number}")

        # Without re-evaluation
        review_desc, comments, issues = process_pr(pr_url, reeval_response=False)
        save_review(pr_number, review_desc, comments, issues, no_eval_folder)

        # # With re-evaluation
        # review_desc, comments, topics = process_pr(pr_url, reeval_response=True)
        # save_review(pr_number, review_desc, comments, topics, with_eval_folder)

        logger.info(f"Completed processing PR {pr_number}")

    logger.info("All PRs processed successfully")


if __name__ == "__main__":
    pr_urls = [
        "https://github.com/sauravpanda/applicant-screening/pull/5",
        "https://github.com/Cloud-Code-AI/kaizen/pull/335",
        "https://github.com/Cloud-Code-AI/kaizen/pull/440",
        "https://github.com/Cloud-Code-AI/kaizen/pull/222",
        "https://github.com/Cloud-Code-AI/kaizen/pull/476",
        "https://github.com/Cloud-Code-AI/kaizen/pull/252",
        "https://github.com/Cloud-Code-AI/kaizen/pull/400",
        # "https://github.com/supermemoryai/supermemory/pull/164",
        "https://github.com/supermemoryai/supermemory/pull/232",
        # Add more PR URLs here
    ]
    main(pr_urls)
