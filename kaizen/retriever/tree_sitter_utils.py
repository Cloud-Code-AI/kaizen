import os
from functools import lru_cache
from tree_sitter import Language, Parser
from typing import Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory where the language libraries are stored
LANGUAGE_DIR = "/app/tree_sitter_languages"

class LanguageLoader:
    @staticmethod
    @lru_cache(maxsize=None)
    def load_language(language: str) -> Language:
        try:
            lang_file = os.path.join(LANGUAGE_DIR, f"{language}.so")
            if not os.path.exists(lang_file):
                raise FileNotFoundError(f"Language file for {language} not found.")
            return Language(lang_file, language)
        except Exception as e:
            logger.error(f"Failed to load language {language}: {str(e)}")
            raise

class ParserFactory:
    @staticmethod
    @lru_cache(maxsize=None)
    def get_parser(language: str) -> Parser:
        try:
            parser = Parser()
            lang = LanguageLoader.load_language(language)
            parser.set_language(lang)
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

def parse_code(code: str, language: str) -> Dict[str, Any]:
    try:
        parser = ParserFactory.get_parser(language)
        tree = parser.parse(bytes(code, "utf8"))
        return traverse_tree(tree.root_node, code.encode("utf8"))
    except Exception as e:
        logger.error(f"Failed to parse {language} code: {str(e)}")
        raise

def check_language_files():
    required_languages = ["python", "javascript", "typescript", "rust"]
    missing_languages = []
    for lang in required_languages:
        try:
            LanguageLoader.load_language(lang)
        except FileNotFoundError:
            missing_languages.append(lang)
    
    if missing_languages:
        logger.warning(f"Missing language files for: {', '.join(missing_languages)}")
    else:
        logger.info("All required language files are present.")

# Call this function at the start of your application
check_language_files()