import os
import importlib
import logging
from kaizen.llms.provider import LLMProvider
from kaizen.helpers.parser import extract_json
from kaizen.llms.prompts.unit_tests_prompts import (
    UNIT_TEST_SYSTEM_PROMPT,
    UNIT_TEST_PROMPT,
    REVIEW_UNIT_TEST_PROMPT,
)


class UnitTestGenerator:
    def __init__(self):
        self.output_folder = "./.kaizen/unit_test/"
        self.supported_languages = {
            "py": "PythonParser",
            "js": "JavaScriptParser",
            "ts": "TypeScriptParser",
            "jsx": "ReactParser",
            "tsx": "ReactTSParser",
        }
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=UNIT_TEST_SYSTEM_PROMPT)
        self._create_output_folder()

    def generate_tests(self, file_path: str, content: str = None):
        """
        file_path: (str) - path of file relative to the root of project.
        content: (str) - File Content
        """
        file_extension = file_path.split(".")[-1]
        if file_extension not in self.supported_languages:
            raise ValueError(f"Unsupported file type: .{file_extension}")

        parser_class_name = self.supported_languages[file_extension]
        parser_module = importlib.import_module(
            f"kaizen.parsers.{parser_class_name.lower()}"
        )
        parser_class = getattr(parser_module, parser_class_name)
        parser = parser_class()

        # Load content if its none
        with open(file_path, "r+") as file:
            content = file.read()

        parsed_data = parser.parse(content)
        self.generate_test_files(parsed_data, file_extension, file_path)

    def generate_test_files(self, parsed_data, file_extension, file_path):
        total_usage = self.provider.DEFAULT_USAGE
        for item in parsed_data:
            test_file_name = f"test_{item['name'].lower()}.{file_extension}"
            test_file_path = os.path.join(self.output_folder, test_file_name)
            item["full_path"] = file_path
            ai_generated_tests, usage = self.generate_ai_tests(
                item, source_code=item["source"]
            )
            total_usage = self.provider.update_usage(total_usage, usage)
            tests_json = extract_json(ai_generated_tests)
            self.logger.info(f"ai generated tests: {ai_generated_tests}")
            # test_file_path = tests_json["test_file_name"]
            ai_generated_tests, usage = self.review_ai_generated_tests(
                item, source_code=item["source"], current_tests=tests_json
            )
            total_usage = self.provider.update_usage(total_usage, usage)
            tests_json = extract_json(ai_generated_tests)
            with open(test_file_path, "w") as test_file:
                test_file.write(tests_json["test_file_content"])

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

    def _create_output_folder(self):
        os.makedirs(self.output_folder, exist_ok=True)


if __name__ == "__main__":
    generator = UnitTestGenerator()
    code = '''
class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, a, b):
        """Add two numbers and store the result."""
        self.result = a + b
        return self.result

    def subtract(self, a, b):
        """Subtract b from a and store the result."""
        self.result = a - b
        return self.result

    def get_result(self):
        """Return the last calculated result."""
        return self.result

def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    calc = Calculator()
    print(calc.add(5, 3))  # Should print 8
    print(calc.subtract(10, 4))  # Should print 6
    print(calc.get_result())  # Should print 6
    print(greet("Alice"))  # Should print "Hello, Alice!"
'''
    # generator.generate_tests(file_path="sample.py", content=code)  # Replace with the actual file path
    generator.generate_tests(file_path="kaizen/helpers/output.py")
