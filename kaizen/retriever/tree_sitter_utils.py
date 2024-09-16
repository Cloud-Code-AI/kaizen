import tree_sitter_python
import tree_sitter_javascript
import tree_sitter_typescript
import tree_sitter_rust
from tree_sitter import Language, Parser
from typing import Dict, Any
import logging
from functools import lru_cache


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PY_LANGUAGE = Language(tree_sitter_python.language())
JS_LANGUAGE = Language(tree_sitter_javascript.language())
TS_LANGUAGE = Language(tree_sitter_typescript.language_typescript())
TSX_LANGUAGE = Language(tree_sitter_typescript.language_tsx())
RUST_LANGUAGE = Language(tree_sitter_rust.language())


class LanguageLoader:
    @staticmethod
    @lru_cache(maxsize=None)
    def load_language(language: str) -> Language:
        language_map = {
            "python": PY_LANGUAGE,
            "javascript": JS_LANGUAGE,
            "typescript": TS_LANGUAGE,
            "rust": RUST_LANGUAGE,
        }
        lang = language.replace("tree-sitter-", "")
        if lang not in language_map:
            raise ValueError(f"Unsupported language: {language}")
        return language_map[lang]


class ParserFactory:
    @staticmethod
    @lru_cache(maxsize=None)
    def get_parser(language: str) -> Parser:
        try:
            parser = Parser()
            lang = LanguageLoader.load_language(language)
            parser.language = lang
            return parser
        except Exception as e:
            logger.error(f"Failed to create parser for {language}: {str(e)}")
            raise


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
            "start_line": node.start_point[0],
            "end_line": node.end_point[0],
        }
    elif node.type in ["class_definition", "class_declaration"]:
        return {
            "type": "class",
            "name": node.child_by_field_name("name").text.decode("utf8"),
            "code": code_bytes[node.start_byte : node.end_byte].decode("utf8"),
            "start_line": node.start_point[0],
            "end_line": node.end_point[0],
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
            "start_line": node.start_point[0],
            "end_line": node.end_point[0],
        }
    elif node.type == "impl_item":
        return {
            "type": "impl",
            "name": node.child_by_field_name("type").text.decode("utf8"),
            "code": code_bytes[node.start_byte : node.end_byte].decode("utf8"),
            "start_line": node.start_point[0],
            "end_line": node.end_point[0],
        }
    else:
        return None


def parse_code(node: Any, code_bytes: bytes) -> Dict[str, Any]:
    try:
        return traverse_tree(node, code_bytes)
    except Exception as e:
        logger.error(f"Failed to parse code: {str(e)}")
        raise


def check_language_files():
    required_languages = ["python", "javascript", "typescript", "rust"]
    missing_languages = []
    for lang in required_languages:
        try:
            LanguageLoader.load_language(lang)
        except Exception as e:
            logger.warning(f"Failed to load language {lang}: {str(e)}")
            missing_languages.append(lang)

    if missing_languages:
        logger.warning(
            f"Missing or failed to load language files for: {', '.join(missing_languages)}"
        )
    else:
        logger.info("All required language files are present and loaded successfully.")


# Call this function at the start of your application
check_language_files()
