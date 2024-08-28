import json
from pathlib import Path


def print_issues_for_pr(pr_number):
    base_path = Path(".experiments/code_review")
    models = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4o-try2",
        "haiku",
        "llama-405b",
        "sonnet-3.5",
    ]

    for model in models:
        file_path = base_path / model / "no_eval" / f"pr_{pr_number}" / "issues.json"

        if file_path.exists():
            print(f"\nModel: {model}")
            print(f"File: {file_path}")

            try:
                with open(file_path, "r") as file:
                    data = json.load(file)
                    formatted_json = json.dumps(data, indent=2)
                    print("Content:")
                    print(formatted_json)
            except json.JSONDecodeError:
                print("Error: Invalid JSON file")
            except Exception as e:
                print(f"Error reading file: {str(e)}")
        else:
            print(f"\nModel: {model}")
            print(f"File not found: {file_path}")


# Example usage
pr_number = 476
print_issues_for_pr(pr_number)
