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
    pattern = r"```(?:\w+)?\n([\s\S]*?)\n```"
    match = re.search(pattern, text)
    if match:
        return match.group(1).strip()
    return text


def patch_to_separate_chunks(patch_text):
    lines = patch_text.split("\n")
    removals = []
    additions = []
    metadata = []
    removal_line_num = 0
    addition_line_num = 0
    unedited_count = 0
    current_hunk = None
    is_diff = False

    for line in lines:
        if "diff --git" in line:
            is_diff = True
            removals.append("~~~~~~~~~~")
            additions.append("~~~~~~~~~~")
        elif is_diff:
            is_diff = False
        elif line.startswith("@"):
            if current_hunk:
                metadata.append(current_hunk)
            current_hunk = line
            match = re.match(r"@@ -(\d+),\d+ \+(\d+),\d+ @@", line)
            if match:
                removal_line_num = int(match.group(1))
                addition_line_num = int(match.group(2))
                removals.append("=====")
                additions.append("=====")
        elif line.startswith("---"):
            removals.append(f"{0:<4} {line}")
        elif line.startswith("+++"):
            additions.append(f"{0:<4} {line}")
        elif line.startswith("-"):
            removals.append(f"{removal_line_num:<4} {line}")
            removal_line_num += 1
        elif line.startswith("+"):
            additions.append(f"{addition_line_num:<4} {line}")
            addition_line_num += 1
        else:
            removals.append(f"{removal_line_num:<4} {line}")
            additions.append(f"{addition_line_num:<4} {line}")
            removal_line_num += 1
            addition_line_num += 1
            unedited_count += 1

    if current_hunk:
        metadata.append(current_hunk)

    output = ["Metadata:"]
    output.extend(metadata)
    output.append(f"\nRemovals: (including {unedited_count} unedited lines)")
    output.extend(removals)
    output.append(f"\nAdditions: (including {unedited_count} unedited lines)")
    output.extend(additions)

    return "\n".join(output)
