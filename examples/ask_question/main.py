from kaizen.reviewer.ask_question import QuestionAnswer
from kaizen.llms.provider import LLMProvider
from github_app.github_helper.utils import get_diff_text, get_pr_files
import json
import logging

logging.basicConfig(level="DEBUG")

# PR details
pr_diff = "https://github.com/Cloud-Code-AI/kaizen/pull/335.patch"
pr_files = "https://api.github.com/repos/Cloud-Code-AI/kaizen/pulls/335/files"
pr_title = "feat: updated the prompt to provide solution"

# Fetch PR data
diff_text = get_diff_text(pr_diff, "")
pr_files = get_pr_files(pr_files, "")

# Initialize QuestionAnswer
qa = QuestionAnswer(llm_provider=LLMProvider())

# Example questions
questions = [
    "What are the main changes in this pull request?",
    "Are there any potential performance implications in these changes?",
    "Does this PR introduce any new dependencies?",
]

# Ask questions about the PR
for question in questions:
    print(f"\n----- Question: {question} -----")

    answer_output = qa.ask_pull_request(
        diff_text=diff_text,
        pull_request_title=pr_title,
        pull_request_desc="",
        question=question,
        pull_request_files=pr_files,
        user="kaizen/example",
    )

    print(f"Answer: {answer_output.answer}")
    print(f"Model: {answer_output.model_name}")
    print(f"Usage: {json.dumps(answer_output.usage, indent=2)}")
    print(f"Cost: {json.dumps(answer_output.cost, indent=2)}")

# Check if a specific question's prompt is within token limit
sample_question = "What are the coding style changes in this PR?"
is_within_limit = qa.is_ask_question_prompt_within_limit(
    diff_text=diff_text,
    pull_request_title=pr_title,
    pull_request_desc="",
    question=sample_question,
)
print(f"\nIs the prompt for '{sample_question}' within token limit? {is_within_limit}")
