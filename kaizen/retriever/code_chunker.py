from typing import Dict, Any
from kaizen.retriever.tree_sitter_utils import parse_code, ParserFactory

ParsedBody = Dict[str, Dict[str, Any]]


def chunk_code(code: str, language: str) -> ParsedBody:
    parser = ParserFactory.get_parser(language)
    tree = parser.parse(code.encode("utf8"))

    body: ParsedBody = {
        "functions": {},
        "classes": {},
        "hooks": {},
        "components": {},
        "other_blocks": [],
    }
    # code_bytes = code.encode("utf8")

    def process_node(node):
        result = parse_code(code, language)
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
