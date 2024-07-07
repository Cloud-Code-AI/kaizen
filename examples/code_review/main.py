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

pr_diff = "https://github.com/Cloud-Code-AI/kaizen/pull/146.diff"
pr_files = "https://api.github.com/repos/Cloud-Code-AI/kaizen/pulls/146/files"
pr_title = "feat: updated the prompt to provide solution"

diff_text = get_diff_text(pr_diff, "")
pr_files = get_pr_files(pr_files, "")
print("diff: ", diff_text)
print("pr_files", pr_files)


reviewer = CodeReviewer(llm_provider=LLMProvider())
review_data = reviewer.review_pull_request(
    diff_text=diff_text,
    pull_request_title=pr_title,
    pull_request_desc="",
    pull_request_files=pr_files,
    user="kaizen/example",
)

pr_desc = PRDescriptionGenerator(llm_provider=LLMProvider())
topics = clean_keys(review_data.topics, "important")
review_desc = create_pr_review_text(topics)
comments, topics = create_review_comments(topics)

print(f"Raw Topics: \n {json.dumps(topics, indent=2)}\n")
print(f"GENERATED REVIEW: \n {review_desc}")
print(f"\nComment and topics: \n {comments}, \n{topics}")
print(review_data)
print("---------------Generate desc-------------")
desc_data = pr_desc.generate_pull_request_desc(
    diff_text=diff_text,
    pull_request_title=pr_title,
    pull_request_desc="",
    pull_request_files=pr_files,
    user="kaizen/example",
)
print(desc_data)