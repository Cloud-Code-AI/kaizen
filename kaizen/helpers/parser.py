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


def patch_to_numbered_lines(patch_text):
    lines = patch_text.split("\n")
    additions = []
    metadata = []
    addition_line_num = 0
    unedited_count = 0
    current_hunk = None
    is_diff = False
    first_transition = True
    current_file_name = ""
    for line in lines:
        if "diff --git" in line:
            is_diff = True
            if first_transition:
                additions = []
                first_transition = False
                continue
            additions.append("\n</change_block>\n\n")

        elif is_diff:
            is_diff = False
        elif line.startswith("@"):
            if current_hunk:
                metadata.append(current_hunk)
            current_hunk = line
            match = re.match(r"@@ -(\d+),\d+ \+(\d+),\d+ @@", line)
            if match:
                addition_line_num = int(match.group(2))
                additions.append("\n<change_block>\n")
                additions.append(f"Filename: {current_file_name}\n")
        elif line.startswith("---"):
            line = line.replace("a/", "").replace("b/", "").replace("--- ", "")
            current_file_name = line
        elif line.startswith("+++"):
            line = line.replace("a/", "").replace("b/", "").replace("+++ ", "")
            current_file_name = line
        elif line.startswith("-"):
            line = "<-> " + line[1:]
        elif line.startswith("+"):
            line = line[1:]
            additions.append(f"{addition_line_num:<5} {line}")
            addition_line_num += 1
        else:
            addition_line_num += 1
            unedited_count += 1

    if current_hunk:
        metadata.append(current_hunk)
        additions.append("\n</change_block>")

    output = []
    output.append(f"\n\n\n##Additions: (including {unedited_count} unedited lines)\n")
    output.extend(additions)

    return "\n".join(output)


def format_change(old_num, new_num, change_type, content, ignore_deletions=False):
    old_num_str = f"{old_num:<5}" if old_num is not None else "_    "
    new_num_str = f"{new_num:<5}" if new_num is not None else "_    "
    if ignore_deletions:
        old_num_str = "_    "
    return f"{old_num_str} {new_num_str} {change_type} {content}"


def patch_to_combined_chunks(patch_text, ignore_deletions=False):
    lines = patch_text.split("\n")
    changes = []
    metadata = []
    removal_line_num = 0
    addition_line_num = 0
    unedited_removal_num = 0
    unedited_addition_num = 0
    unedited_count = 0
    current_hunk = None
    is_diff = False
    first_transition = True
    current_file_name = ""

    for line in lines:
        if "diff --git" in line:
            is_diff = True
            if not first_transition:
                changes.append("\n</change_block>\n\n")
            first_transition = False

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
                unedited_removal_num = removal_line_num
                unedited_addition_num = addition_line_num
                if changes and "\n<change_block>" not in changes:
                    changes = []
                changes.append("\n<change_block>")
                changes.append(
                    f"\n<file_start>\nFilename: {current_file_name}\n<file_end>\n"
                )
        elif line.startswith("index "):
            continue
        elif line.startswith("---"):
            line = line.replace("a/", "").replace("b/", "").replace("--- ", "")
            current_file_name = line
        elif line.startswith("+++"):
            line = line.replace("a/", "").replace("b/", "").replace("+++ ", "")
            current_file_name = line
        elif line.startswith("-"):
            content = line[1:]
            if not ignore_deletions:
                changes.append(
                    format_change(
                        removal_line_num, None, "-1:[-]", content, ignore_deletions
                    )
                )
            removal_line_num += 1
            unedited_removal_num = removal_line_num
        elif line.startswith("+"):
            content = line[1:]
            changes.append(
                format_change(
                    None, addition_line_num, "+1:[+]", content, ignore_deletions
                )
            )
            addition_line_num += 1
            unedited_addition_num = addition_line_num
        else:
            content = line
            changes.append(
                format_change(
                    unedited_removal_num,
                    unedited_addition_num,
                    " 0:[.]",
                    content,
                    ignore_deletions,
                )
            )
            unedited_removal_num += 1
            unedited_addition_num += 1
            removal_line_num += 1
            addition_line_num += 1
            unedited_count += 1

    if current_hunk:
        metadata.append(current_hunk)
        changes.append("\n</change_block>\n\n")

    output = changes

    return "\n".join(output)


def format_add_linenum(new_num, content, ignore_deletions=False):
    new_num_str = f"{new_num:<5}" if new_num is not None else "     "
    return f"{new_num_str} {content}"
