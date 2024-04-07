import json


def extract_json(text):
    # Find the start and end positions of the JSON data
    start_index = text.find("{")
    end_index = text.rfind("}") + 1

    # Extract the JSON data from the text
    json_data = text[start_index:end_index]
    json_data = json_data.replace("\n}", "}")
    json_data = json_data.replace("\n", "\\n")
    json_data = json_data.replace("\'", "")

    # Parse the JSON data
    parsed_data = json.loads(json_data)
    return parsed_data
