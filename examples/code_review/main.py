from kaizen.reviewer.code_review import CodeReviewer
from kaizen.generator.pr_description import PRDescriptionGenerator
from kaizen.helpers.output import create_pr_review_text
from kaizen.llms.provider import LLMProvider
from github_app.github_helper.utils import get_diff_text, get_pr_files
from github_app.github_helper.pull_requests import (
    clean_keys,
    create_review_comments,
)
import json
import logging

logging.basicConfig(level="DEBUG")

pr_diff = "https://github.com/Cloud-Code-AI/kaizen/pull/335.patch"
pr_files = "https://api.github.com/repos/Cloud-Code-AI/kaizen/pulls/335/files"
pr_title = "feat: updated the prompt to provide solution"

diff_text = get_diff_text(pr_diff, "")
pr_files = get_pr_files(pr_files, "")
# print("diff: ", diff_text)
# print("pr_files", pr_files)


reviewer = CodeReviewer(llm_provider=LLMProvider())
review_data = reviewer.review_pull_request(
    diff_text=diff_text,
    pull_request_title=pr_title,
    pull_request_desc="",
    pull_request_files=pr_files,
    user="kaizen/example",
    reeval_response=False,
    custom_prompt="Changes in prompt should be marked critical with high severity",
)

topics = clean_keys(review_data.topics, "important")
review_desc = create_pr_review_text(topics)
comments, topics = create_review_comments(topics)

print(f"Raw Topics: \n {json.dumps(topics, indent=2)}\n")
print(f"GENERATED REVIEW: \n {review_desc}")
print(f"\nComment and topics: \n {json.dumps(comments, indent=2)}, \n{topics}")


print("---------------Generate desc-------------")
pr_desc = PRDescriptionGenerator(llm_provider=LLMProvider())
desc_data = pr_desc.generate_pull_request_desc(
    diff_text=None,
    pull_request_title=pr_title,
    pull_request_desc="",
    pull_request_files=pr_files,
    user="kaizen/example",
)
print(desc_data)
