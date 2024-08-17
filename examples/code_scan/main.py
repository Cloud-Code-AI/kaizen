from kaizen.reviewer.code_scan import CodeScanner
from kaizen.llms.provider import LLMProvider
import json

filename = "github_app/main.py"
with open(filename, "r+") as f:
    file_data = f.read()

reviewer = CodeScanner(llm_provider=LLMProvider())
dir_path = "github_app/"
# Scan a Single file:
# review_data = reviewer.review_code(file_data=file_data, user="Example/CodeScan")

# Scan a Whole repo
review_data = reviewer.review_code_dir(
    dir_path=dir_path, reevaluate=True, user="Example/CodeScan"
)
print(f"Total {len(review_data.issues)} Issues found!!!!")
print(json.dumps(review_data.issues, indent=2))
