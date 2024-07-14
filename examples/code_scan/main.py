from kaizen.reviewer.code_scan import CodeScanner
from kaizen.llms.provider import LLMProvider

filename = "github_app/main.py"
with open(filename, "r+") as f:
    file_data = f.read()

reviewer = CodeScanner(llm_provider=LLMProvider())
review_data = reviewer.review_code(file_data=file_data, user="Example/CodeScan")

print(review_data)
