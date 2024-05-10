import json
import re

EXCLUDED_FILETYPES = ["json", "css", "xml"]


def extract_json(text):
    # Find the start and end positions of the JSON data
    start_index = text.find("{")
    end_index = text.rfind("}") + 1

    # Extract the JSON data from the text
    json_data = text[start_index:end_index]
    json_data = re.sub(r"\s*\\*\n*\s*{\s*\\*\n*\s*", "{", json_data)
    json_data = re.sub(r"\s*\\*\n*\s*\[\s*\\*\n*\s*", "[", json_data)
    json_data = re.sub(r"\s*\\*\n*\s*}\s*\\*\n*\s*", "}", json_data)
    json_data = re.sub(r"\s*\\*\n\s*\]\s*\\*\n\s*", "]", json_data)
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
