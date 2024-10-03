from kaizen.reviewer.code_review import CodeReviewer
from kaizen.generator.pr_description import PRDescriptionGenerator
from kaizen.llms.provider import LLMProvider
from github_app.github_helper.utils import get_diff_text, get_pr_files
import logging
from kaizen.formatters.code_review_formatter import (
    create_pr_review_text,
    filter_and_categorize_issues,
)

logging.basicConfig(level="DEBUG")

pr_diff = "https://github.com/Cloud-Code-AI/kaizen/pull/559.patch"
pr_files = "https://api.github.com/repos/Cloud-Code-AI/kaizen/pulls/559/files"
pr_title = "feat: updated the prompt to provide solution"

diff_text = get_diff_text(pr_diff, "")
pr_files = get_pr_files(pr_files, "")
# print("diff: ", diff_text)
# print("pr_files", pr_files)

custom_rule = """
All the function names should be in CamelCase.
"""
reviewer = CodeReviewer(llm_provider=LLMProvider())
review_data = reviewer.review_pull_request(
    diff_text=diff_text,
    pull_request_title=pr_title,
    pull_request_desc="",
    pull_request_files=pr_files,
    reeval_response=False,
    custom_rules=custom_rule,
)

comments, issues, is_critical = filter_and_categorize_issues(data=review_data.issues)
review_desc = create_pr_review_text(
    review_data.issues, code_quality=review_data.code_quality
)
print(f"GENERATED REVIEW: \n {review_desc}")
print(f"Cleaned issues: ", issues)
print(f"All issues:", review_data.issues)

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

comit_message = pr_desc.generate_pr_commit_message(desc_data.desc)
print(comit_message)
