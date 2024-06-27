import json
import re

EXCLUDED_FILETYPES = ["json"]


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


def extract_json_with_llm_retry(provider, text, total_usage):
    # TODO: Update this functionality
    # try:
    #     json_data = extract_json(text)
    #     return json_data, total_usage
    # except Exception as e:
    #     print(f"Error parsing json: {e}")
    #     prompt = f"Help me fix this json data: {text}"
    #     resp, usage = provider.chat_completion(prompt)
    #     total_usage = provider.update_usage(total_usage, usage)
    #     json_data = extract_json(resp)
    #     return json_data, total_usage
    json_data = extract_json(text)
    return json_data, total_usage


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
