import os
import subprocess
from tree_sitter import Language, Parser
from typing import Dict, List, Any

ParsedBody = Dict[str, Dict[str, Any]]

# Define the languages and their GitHub repositories
LANGUAGES = {
    "python": "https://github.com/tree-sitter/tree-sitter-python",
    "javascript": "https://github.com/tree-sitter/tree-sitter-javascript",
    "typescript": "https://github.com/tree-sitter/tree-sitter-typescript",
    "rust": "https://github.com/tree-sitter/tree-sitter-rust",
}

# Directory to store the language libraries
LANGUAGE_DIR = os.path.join(os.path.dirname(__file__), "tree_sitter_languages")


def ensure_language_installed(language: str) -> None:
    if not os.path.exists(LANGUAGE_DIR):
        os.makedirs(LANGUAGE_DIR)

    lang_file = os.path.join(LANGUAGE_DIR, f"{language}.so")
    if not os.path.exists(lang_file):
        repo_url = LANGUAGES[language]
        repo_dir = os.path.join(LANGUAGE_DIR, f"tree-sitter-{language}")

        if not os.path.exists(repo_dir):
            subprocess.run(["git", "clone", repo_url, repo_dir], check=True)

        subprocess.run(
            ["bash", "-c", f"cd {repo_dir} && git submodule update --init"], check=True
        )
        Language.build_library(lang_file, [repo_dir])


def get_parser(language: str) -> Parser:
    ensure_language_installed(language)
    parser = Parser()
    lang_file = os.path.join(LANGUAGE_DIR, f"{language}.so")
    lang = Language(lang_file, language)
    parser.set_language(lang)
    return parser


def traverse_tree(node, code_bytes: bytes) -> Dict[str, Any]:
    if node.type in [
        "function_definition",
        "function_declaration",
        "arrow_function",
        "method_definition",
    ]:
        return {
            "type": "function",
            "name": (
                node.child_by_field_name("name").text.decode("utf8")
                if node.child_by_field_name("name")
                else "anonymous"
            ),
            "code": code_bytes[node.start_byte : node.end_byte].decode("utf8"),
        }
    elif node.type in ["class_definition", "class_declaration"]:
        return {
            "type": "class",
            "name": node.child_by_field_name("name").text.decode("utf8"),
            "code": code_bytes[node.start_byte : node.end_byte].decode("utf8"),
        }
    elif node.type in ["jsx_element", "jsx_self_closing_element"]:
        return {
            "type": "component",
            "name": (
                node.child_by_field_name("opening_element")
                .child_by_field_name("name")
                .text.decode("utf8")
                if node.type == "jsx_element"
                else node.child_by_field_name("name").text.decode("utf8")
            ),
            "code": code_bytes[node.start_byte : node.end_byte].decode("utf8"),
        }
    elif node.type == "impl_item":
        return {
            "type": "impl",
            "name": node.child_by_field_name("type").text.decode("utf8"),
            "code": code_bytes[node.start_byte : node.end_byte].decode("utf8"),
        }
    else:
        return None


def chunk_code(code: str, language: str) -> ParsedBody:
    parser = get_parser(language)
    tree = parser.parse(code.encode("utf8"))

    body: ParsedBody = {
        "functions": {},
        "classes": {},
        "hooks": {},
        "components": {},
        "other_blocks": [],
    }
    code_bytes = code.encode("utf8")

    def process_node(node):
        result = traverse_tree(node, code_bytes)
        if result:
            if result["type"] == "function":
                if is_react_hook(result["name"]):
                    body["hooks"][result["name"]] = result["code"]
                elif is_react_component(result["code"]):
                    body["components"][result["name"]] = result["code"]
                else:
                    body["functions"][result["name"]] = result["code"]
            elif result["type"] == "class":
                if is_react_component(result["code"]):
                    body["components"][result["name"]] = result["code"]
                else:
                    body["classes"][result["name"]] = result["code"]
            elif result["type"] == "component":
                body["components"][result["name"]] = result["code"]
            elif result["type"] == "impl":
                body["classes"][result["name"]] = result["code"]
        else:
            for child in node.children:
                process_node(child)

    process_node(tree.root_node)

    # Collect remaining code as other_blocks
    collected_ranges = []
    for section in body.values():
        if isinstance(section, dict):
            for code_block in section.values():
                start = code.index(code_block)
                collected_ranges.append((start, start + len(code_block)))

    collected_ranges.sort()
    last_end = 0
    for start, end in collected_ranges:
        if start > last_end:
            body["other_blocks"].append(code[last_end:start].strip())
        last_end = end
    if last_end < len(code):
        body["other_blocks"].append(code[last_end:].strip())

    return body


def is_react_hook(name: str) -> bool:
    return name.startswith("use") and len(name) > 3 and name[3].isupper()


def is_react_component(code: str) -> bool:
    return (
        "React" in code or "jsx" in code.lower() or "tsx" in code.lower() or "<" in code
    )
