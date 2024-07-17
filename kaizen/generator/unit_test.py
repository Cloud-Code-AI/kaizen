import os
import importlib
import logging
from kaizen.llms.provider import LLMProvider
from kaizen.helpers.parser import extract_json, extract_code_from_markdown
from kaizen.llms.prompts.unit_tests_prompts import (
    UNIT_TEST_SYSTEM_PROMPT,
    UNIT_TEST_PROMPT,
    REVIEW_UNIT_TEST_PROMPT,
    REVIEW_TEST_CASE_PROMPT,
)


class UnitTestGenerator:
    def __init__(self):
        self.output_folder = "./.kaizen/unit_test/"
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        self.supported_languages = {
            "py": "PythonParser",
            "js": "JavaScriptParser",
            "ts": "TypeScriptParser",
            "jsx": "ReactParser",
            "tsx": "ReactTSParser",
        }
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=UNIT_TEST_SYSTEM_PROMPT)
        self._create_output_folder(self.output_folder)

    def generate_tests(
        self, file_path: str, content: str = None, output_path: str = None
    ):
        """
        file_path: (str) - path of file relative to the root of project.
        content: (str) - File Content
        """
        if output_path:
            self.output_folder = output_path
        file_extension = file_path.split(".")[-1]
        if file_extension not in self.supported_languages:
            raise ValueError(f"Unsupported file type: .{file_extension}")

        parser_class_name = self.supported_languages[file_extension]
        parser_module = importlib.import_module(
            f"kaizen.parsers.{parser_class_name.lower()}"
        )
        parser_class = getattr(parser_module, parser_class_name)
        parser = parser_class()

        if not content:
            with open(file_path, "r+") as file:
                content = file.read()

        parsed_data = parser.parse(content)
        self.generate_test_files(parsed_data, file_extension, file_path)
        return {}, self.total_usage

    def generate_test_files(self, parsed_data, file_extension, file_path):
        folder_path = "/".join(file_path.split("/")[:-1])
        self.total_usage = self.provider.DEFAULT_USAGE
        for item in parsed_data:
            test_file_name = f"test_{item['name'].lower()}.{file_extension}"
            test_file_path = os.path.join(
                self.output_folder, folder_path, test_file_name
            )
            self._create_output_folder("/".join(test_file_path.split("/")[:-1]))
            item["full_path"] = file_path
            ai_generated_tests, usage = self.generate_ai_tests(
                item, source_code=item["source"]
            )
            self.total_usage = self.provider.update_usage(self.total_usage, usage)
            tests_json = extract_json(ai_generated_tests)
            self.logger.debug(f"ai generated tests: {ai_generated_tests}")
            # test_file_path = tests_json["test_file_name"]
            # ai_generated_tests, usage = self.review_ai_generated_tests(
            #     item, source_code=item["source"], current_tests=tests_json
            # )
            # self.total_usage = self.provider.update_usage(self.total_usage, usage)
            # tests_json = extract_json(ai_generated_tests)

            # Review File Content

            test_code, usage = self.review_test_file(
                test_file_name, tests_json["test_file_content"]
            )
            self.total_usage = self.provider.update_usage(self.total_usage, usage)
            test_code = extract_code_from_markdown(test_code)
            with open(test_file_path, "w") as test_file:
                test_file.write(test_code)

    def generate_ai_tests(self, item, source_code):
        prompt = UNIT_TEST_PROMPT.format(
            SOURCE_CODE=source_code,
            ITEM_TYPE=item["type"],
            ITEM_NAME=item["name"],
            FULL_FILE_PATH=item["full_path"],
        )
        response, usage = self.provider.chat_completion(prompt, model="best")
        return response, usage

    def review_ai_generated_tests(self, item, source_code, current_tests):
        prompt = REVIEW_UNIT_TEST_PROMPT.format(
            SOURCE_CODE=source_code,
            ITEM_TYPE=item["type"],
            ITEM_NAME=item["name"],
            FULL_FILE_PATH=item["full_path"],
            CURRENT_TEST=current_tests["test_file_content"],
        )
        response, usage = self.provider.chat_completion(prompt, model="best")
        return response, usage

    def review_test_file(self, file_name, test_code):
        file_content_prompt = REVIEW_TEST_CASE_PROMPT.format(
            FILE_NAME=file_name, CODE=test_code
        )
        response, usage = self.provider.chat_completion(
            file_content_prompt, model="best"
        )
        return response, usage

    def _create_output_folder(self, folder_name):
        os.makedirs(folder_name, exist_ok=True)
