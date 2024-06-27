from kaizen.reviewer.work_summarizer import WorkSummaryGenerator
import requests
from datetime import datetime, timedelta, timezone

# GitHub repository information
GITHUB_OWNER = "Cloud-Code-AI"
GITHUB_REPO_NAME = "kaizen"

# Get the current date and calculate the date 14 days ago
current_date = datetime.now(timezone.utc).date()
since_date = current_date - timedelta(days=7)

# Convert the date to ISO format
since_date_iso = since_date.isoformat()

# GitHub API endpoint for getting commits
commits_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO_NAME}/commits"

# Add query parameters for the since date
params = {"since": since_date_iso}

# Make the API request
commits_response = requests.get(commits_url, params=params)

# Check if the request was successful
if commits_response.status_code != 200:
    print("ERROR: Could not get GitHub commits")
    exit(1)

commits = commits_response.json()

# Get the SHA hashes of the first and last commits
first_commit_sha = commits[0]["sha"]
last_commit_sha = commits[-1]["sha"]

headers = {"Accept": "application/vnd.github.v3+json"}

# Get the diff between the first and last commits
diff_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO_NAME}/compare/{last_commit_sha}...{first_commit_sha}"
diff_response = requests.get(diff_url, headers=headers)
diff_data = diff_response.json()

# Extract file diffs
file_diffs = []
for file_dict in diff_data["files"]:
    if "patch" in file_dict:
        file_diffs.append(
            {
                "file": file_dict["filename"],
                "patch": file_dict["patch"],
                "status": file_dict["status"],
            }
        )

work_summary_generator = WorkSummaryGenerator()
result = work_summary_generator.generate_work_summaries(file_diffs, user="oss_example")
summary = result["summary"]

twitter_post, _ = work_summary_generator.generate_twitter_post(summary, user="oss_example")
linkedin_post, _ = work_summary_generator.generate_linkedin_post(
    summary, user="oss_example"
)

print(f" Work Summary: \n {summary}\n")

print(f" Twitter Post: \n {twitter_post}\n")
print(f" LinkedIn Post: \n {linkedin_post}\n")
