from typing import Dict, Any
from kaizen.retriever.tree_sitter_utils import parse_code, ParserFactory
import os

ParsedBody = Dict[str, Dict[str, Any]]


def chunk_code(code: str, language: str) -> ParsedBody:
    parser = ParserFactory.get_parser(language)
    tree = parser.parse(code.encode("utf8"))
    code_bytes = code.encode("utf8")
    body: ParsedBody = {
        "imports": [],
        "global_variables": [],
        "type_definitions": [],
        "functions": {},
        "async_functions": {},
        "classes": {},
        "hooks": {},
        "components": {},
        "jsx_elements": [],
        "other_blocks": [],
    }

    def process_node(node):
        result = parse_code(node, code_bytes)
        if result:
            start_line = result.get("start_line", 0)
            end_line = result.get("end_line", 0)

            if result["type"] == "import_statement":
                body["imports"].append(
                    {
                        "code": result["code"],
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                )
            elif (
                result["type"] == "variable_declaration"
                and node.parent.type == "program"
            ):
                body["global_variables"].append(
                    {
                        "code": result["code"],
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                )
            elif result["type"] in ["type_alias", "interface_declaration"]:
                body["type_definitions"].append(
                    {
                        "name": result["name"],
                        "code": result["code"],
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                )
            elif result["type"] == "function":
                if is_react_hook(result["name"]):
                    body["hooks"][result["name"]] = {
                        "code": result["code"],
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                elif is_react_component(result["code"]):
                    body["components"][result["name"]] = {
                        "code": result["code"],
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                elif "async" in result["code"].split()[0]:
                    body["async_functions"][result["name"]] = {
                        "code": result["code"],
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                else:
                    body["functions"][result["name"]] = {
                        "code": result["code"],
                        "start_line": start_line,
                        "end_line": end_line,
                    }
            elif result["type"] == "class":
                if is_react_component(result["code"]):
                    body["components"][result["name"]] = {
                        "code": result["code"],
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                else:
                    body["classes"][result["name"]] = {
                        "code": result["code"],
                        "start_line": start_line,
                        "end_line": end_line,
                    }
            elif result["type"] == "jsx_element":
                body["jsx_elements"].append(
                    {
                        "code": result["code"],
                        "start_line": start_line,
                        "end_line": end_line,
                    }
                )
        else:
            for child in node.children:
                process_node(child)

    process_node(tree.root_node)

    # Collect remaining code as other_blocks
    collected_ranges = []
    for section in body.values():
        if isinstance(section, dict):
            for code_block in section.values():
                collected_ranges.append(
                    (code_block["start_line"], code_block["end_line"])
                )
        elif isinstance(section, list):
            for code_block in section:
                collected_ranges.append(
                    (code_block["start_line"], code_block["end_line"])
                )

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
        "React" in code
        or "jsx" in code.lower()
        or "tsx" in code.lower()
        or "<" in code
        or "props" in code
        or "render" in code
    )


def clean_filename(filepath):
    # Split the path into components
    path_components = filepath.split(os.sep)

    # Find the index of 'tmp' in the path
    try:
        tmp_index = path_components.index("tmp")
    except ValueError:
        # If 'tmp' is not found, return the original filepath
        return filepath

    # Join the components after 'tmp' to create the cleaned filename
    cleaned_filename = os.sep.join(path_components[tmp_index + 2 :])

    return cleaned_filename
