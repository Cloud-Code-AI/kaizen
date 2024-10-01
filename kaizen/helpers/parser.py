import json
import re
import os

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
    # Add any other specific extensions you want to exclude
]

# List of folders to exclude
EXCLUDED_FOLDERS = [
    "node_modules",
    "dist",
    "out",
    "vendor",
    "target",
    "build",
    "__pycache__",
    ".git",
    # Add any other folders you want to exclude
]


def should_ignore_file(filepath):
    """
    Check if a file should be ignored based on its path, name, or extension.

    :param filepath: The full path of the file to check
    :return: True if the file should be ignored, False otherwise
    """
    # Get the file name and extension
    filename = os.path.basename(filepath)
    _, extension = os.path.splitext(filename)
    extension = extension.lstrip(".")  # Remove the leading dot

    # Check if the file is in an excluded folder
    for folder in EXCLUDED_FOLDERS:
        if folder in filepath.split(os.path.sep):
            return True

    # Check if the file extension is in the excluded list
    if extension.lower() in EXCLUDED_FILETYPES:
        return True

    # Check for specific filenames
    if filename in [
        "package-lock.json",
        "yarn.lock",
        "Gemfile.lock",
        "composer.lock",
        ".DS_Store",
        "Thumbs.db",
    ]:
        return True

    return False


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
    new_num_str = f"{new_num:<5}" if new_num is not None else "_    "
    return f"[LINE {new_num_str}] [{change_type}] {content}"


def patch_to_combined_chunks(patch_text, ignore_deletions=False):
    if not patch_text:
        return ""
    patch_text = patch_text.replace("\r\n", "\n")
    lines = patch_text.splitlines(keepends=True)
    changes = []
    removal_line_num = 1
    addition_line_num = 1
    is_diff = False
    removed_hunk = False
    current_file_name = ""

    for line in lines:
        line = line.rstrip("\n")
        if "diff --git" in line:
            is_diff = True
            if not removed_hunk:
                changes = []
                removed_hunk = True
            changes.append("\n")
        elif is_diff:
            is_diff = False
        elif line.startswith("@@"):
            match = re.match(r"@@ -(\d+),\d+ \+(\d+),\d+ @@ (.*)", line)
            if match:
                removal_line_num = int(match.group(1))
                addition_line_num = int(match.group(2))
                content = match.group(3)
                changes.append("\n")
                changes.append(
                    format_change(
                        None, addition_line_num, "CONTEXT", content, ignore_deletions
                    )
                )
        elif line.startswith("index "):
            continue
        elif line.startswith("--- a"):
            line = line.replace("--- a/", "")
            current_file_name = line
            if (
                current_file_name != "/dev/null"
                and changes
                and "[FILE_START]" not in changes[-1]
            ):
                changes.append("\n[FILE_END]\n")
                changes.append(f"\n[FILE_START] {current_file_name}\n")
        elif line.startswith("+++ b"):
            line = line.replace("+++ b/", "")
            current_file_name = line
            if (
                current_file_name != "/dev/null"
                and changes
                and "[FILE_START]" not in changes[-1]
            ):
                changes.append("\n[FILE_END]\n")
                changes.append(f"\n[FILE_START] {current_file_name}\n")
        elif line.startswith("-"):
            content = line[1:]
            if not ignore_deletions:
                changes.append(
                    format_change(
                        None, removal_line_num, "REMOVED", content, ignore_deletions
                    )
                )
            removal_line_num += 1
        elif line.startswith("+"):
            content = line[1:]
            changes.append(
                format_change(
                    None, addition_line_num, "UPDATED", content, ignore_deletions
                )
            )
            addition_line_num += 1
        else:
            content = line
            changes.append(
                format_change(
                    None,
                    addition_line_num,
                    "CONTEXT",
                    content,
                    ignore_deletions,
                )
            )
            removal_line_num += 1
            addition_line_num += 1

    output = changes

    return "\n".join(output)


def format_add_linenum(new_num, content, ignore_deletions=False):
    new_num_str = f"{new_num:<5}" if new_num is not None else "     "
    return f"{new_num_str} {content}"
