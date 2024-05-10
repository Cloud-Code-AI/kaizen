# from kaizen.reviewer.work_summarizer import WorkSummarizer
import requests
import json
from datetime import datetime, timedelta, timezone

# Replace with the owner and repository name
OWNER = 'Cloud-Code-AI'
REPO_NAME = 'kaizen'

# Get the current date and calculate the date 5 days ago
today = datetime.now(timezone.utc).date()
week_ago = today - timedelta(days=14)

# Convert the dates to ISO format
since = week_ago.isoformat()

# GitHub API endpoint for getting commits
url = f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/commits"

# Add query parameters for the since date
params = {
    'since': since
}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code != 200:
    # Parse the JSON data
    print("ERROR: Couldnt get github commits")

commits = response.json()

# print(commits[0])

# Get the SHA hashes of the two commits
commit1_sha = commits[0]["sha"]
commit2_sha = commits[-1]["sha"]

headers = {
    # "Authorization": f"token {access_token}",
    "Accept": "application/vnd.github.v3+json"
}
# print(json.dumps(commits))

# Get the diff between the two commits
diff_url = f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/compare/{commit2_sha}...{commit1_sha}"
response = requests.get(diff_url, headers=headers)
diff_data = response.json()

print(diff_url)
# Print the diff
file_diffs = []
for file in diff_data["files"]:
    if "patch" in file:
        file_diffs.append(
            {
                "file": file['filename'],
                "patch": file["patch"],
                "status": file["status"]
            }
        )

print(f"Diff Files: {json.dumps(file_diffs)}")