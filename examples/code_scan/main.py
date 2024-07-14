from kaizen.reviewer.code_scan import CodeScanner
from kaizen.generator.pr_description import PRDescriptionGenerator
from kaizen.helpers.output import create_pr_review_text
from kaizen.llms.provider import LLMProvider
import json

filename = "github_app/main.py"
with open(filename, "r+") as f:
    file_data = f.read()

reviewer = CodeScanner(llm_provider=LLMProvider())
review_data = reviewer.review_code(file_data=file_data, user="Example/CodeScan")

print(review_data)
