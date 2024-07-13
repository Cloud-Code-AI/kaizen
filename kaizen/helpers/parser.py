import json
import re

EXCLUDED_FILETYPES = [
    # Compiled output
    "class",
    "o",
    "obj",
    "exe",
    "dll",
    "pyc",
    "pyo",
    # Package manager files
    "lock",  # Covers package-lock.json, yarn.lock, Gemfile.lock, composer.lock
    # IDE configurations
    "idea",
    "vscode",
    "project",
    "classpath",
    # Build artifacts and dependencies
    "node_modules",
    "vendor",
    "target",
    "build",
    # Binary and large files
    "zip",
    "tar",
    "gz",
    "rar",
    "pdf",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "jpg",
    "jpeg",
    "png",
    "gif",
    "bmp",
    "ico",
    "mp3",
    "mp4",
    "avi",
    "mov",
    # Log files
    "log",
    # Database files
    "db",
    "sqlite",
    # Temporary files
    "tmp",
    "temp",
    # OS-specific files
    "DS_Store",
    "Thumbs.db",
    # Configuration files
    "gitignore",
    "dockerignore",
    # Add any other specific extensions or directory names you want to exclude
]


def extract_json(text):
    # Find the start and end positions of the JSON data
    start_index = text.find("{")
    end_index = text.rfind("}") + 1

    # Extract the JSON data from the text
    json_data = text[start_index:end_index]
    json_data = re.sub(r"\s*\\*\n*\s*{\s*\n*\s*", "{", json_data)
    json_data = re.sub(r"\s*\\*\n*\s*\[\s*\n*\s*", "[", json_data)
    json_data = re.sub(r"\s*\\*\n*\s*}\s*\n*\s*", "}", json_data)
    json_data = re.sub(r"\s*\\*\n\s*\]\s*\n\s*", "]", json_data)
    json_data = re.sub(r",\s*\\*\n\s*", ",", json_data)
    json_data = re.sub(r'"\s*\\*\n\s*', '"', json_data)
    json_data = json_data.replace("\n", "\\n")

    # Parse the JSON data
    parsed_data = json.loads(json_data)
    return parsed_data


def extract_multi_json(text):
    start_index = text.find("[")
    end_index = text.rfind("]") + 1
    json_data = text[start_index:end_index]
    parsed_data = json.loads(json_data)
    return parsed_data


def extract_markdown_content(text: str) -> str:
    match = re.search(r"```([\s\S]*?)```", text)
    if match:
        return match.group(1).strip()
    return ""


def extract_code_from_markdown(text: str) -> str:
    match = re.search(r"```([\s\S]*?)```", text)
    if match:
        return match.group(1).strip()
    return text
