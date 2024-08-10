import requests
import json
import re

def create_prompt(log_data):
    prompt = f"You are an AI assistant tasked with analyzing log data and identifying potential issues or errors. Here is the log data:\n\n{log_data}\n\nPlease analyze the log data and provide a concise summary of any potential issues or errors detected, along with their severity (e.g., low, medium, high), timestamp, and any relevant details or context."
    return prompt

def analyze_logs(prompt, ollama_server_url):
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt, "model":"mistral"}
    response = requests.post(ollama_server_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        model_response = response.json()["response"]
        return model_response
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def parse_response(response, log_data):
    lines = response.strip().split("\n")
    parsed_response = []
    log_lines = log_data.strip().split("\n")

    for line in lines:
        line = line.strip()
        if line.startswith("- Potential issue:"):
            issue = {"severity": None, "timestamp": None, "details": []}
            issue_parts = line.split(": ", 1)
            if len(issue_parts) > 1:
                issue["details"].append(issue_parts[1].strip())
            parsed_response.append(issue)
        elif line.startswith("Severity:"):
            severity = line.split(": ", 1)[1].strip().lower()
            parsed_response[-1]["severity"] = severity
        elif line.startswith("Timestamp:"):
            timestamp = line.split(": ", 1)[1].strip()
            parsed_response[-1]["timestamp"] = extract_timestamp(timestamp, log_lines)
        elif parsed_response and line:
            parsed_response[-1]["details"].append(line)

    return parsed_response

def extract_timestamp(timestamp_text, log_lines):
    for line in log_lines:
        if timestamp_text in line:
            match = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line)
            if match:
                return match.group()
    return None

def main():
    log_data = """
    2023-05-25 12:34:56 [ERROR] NullPointerException in com.example.app.service.UserService
    2023-05-25 12:35:12 [WARNING] Low disk space on /var/log (only 10% free)
    2023-05-25 12:36:08 [INFO] Application started successfully
    """

    prompt = create_prompt(log_data)
    ollama_server_url = "http://your-ollama-server.com/analyze"

    model_response = analyze_logs(prompt, ollama_server_url)
    if model_response:
        parsed_response = parse_response(model_response, log_data)
        print(json.dumps(parsed_response, indent=2))

if __name__ == "__main__":
    main()