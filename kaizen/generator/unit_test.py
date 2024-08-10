import os
import importlib
import logging
from datetime import datetime
from kaizen.llms.provider import LLMProvider
from kaizen.helpers.parser import extract_json, extract_code_from_markdown
from kaizen.actors.unit_test_runner import UnitTestRunner
from kaizen.llms.prompts.unit_tests_prompts import (
    UNIT_TEST_SYSTEM_PROMPT,
    UNIT_TEST_PLAN_PROMPT,
    REVIEW_UNIT_TEST_PROMPT,
    REVIEW_TEST_CASE_PROMPT,
    PYTHON_UNIT_TEST_PROMPT,
    JAVASCRIPT_UNIT_TEST_PROMPT,
    REACT_UNIT_TEST_PROMPT,
    RUST_UNIT_TEST_PROMPT,
)
from tqdm import tqdm


class UnitTestGenerator:
    def __init__(self, verbose=False):
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
            "rs": "RustParser",
        }
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=UNIT_TEST_SYSTEM_PROMPT)
        self.verbose = verbose
        self.log_dir = "./.kaizen/logs"
        os.makedirs(self.log_dir, exist_ok=True)
        self._create_output_folder(self.output_folder)
        self.max_critique = 3

    def generate_tests(
        self,
        file_path: str,
        content: str = None,
        max_critique: int = 3,
        output_path: str = None,
        verbose: bool = False,
    ):
        """
        file_path: (str) - path of file relative to the root of project.
        content: (str) - File Content
        """
        self.max_critique = max_critique
        if self.verbose:
            self.verbose = verbose
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
        for item in tqdm(parsed_data, desc="Processing Items", unit="item"):
            print(f"\n{'='*50}")
            print(f"Processing Item: {item['name']}")
            print(f"{'='*50}")

            # Step 1: Prepare file name and path
            print("• Preparing file name and path...")
            test_file_name = f"test_{item['name'].lower()}.{file_extension}"
            test_file_path = os.path.join(
                self.output_folder, folder_path, test_file_name
            )
            self._create_output_folder("/".join(test_file_path.split("/")[:-1]))
            item["full_path"] = file_path
            print(f"  ✓ File will be saved as: {test_file_path}")
            self.log_step(
                "Prepare file name and path", f"Test file path: {test_file_path}"
            )

            # Step 2: Generate AI tests
            print("• Generating AI tests...")
            test_code, usage = self.generate_ai_tests(
                item, source_code=item["source"], file_extension=file_extension
            )
            self.total_usage = self.provider.update_usage(self.total_usage, usage)
            print(f"  ✓ AI tests generated successfully")
            self.log_step("Generate AI tests", f"Generated test code:\n{test_code}")
            print(f"  - Initiating Actor Critique Mode with {self.max_critique} max tries")
            counter = 0
            # while counter < self.max_critique:
            #     # Step 3: Review and improve AI tests
            #     print("• Reviewing and improving AI tests...")
            #     requested_improvements, usage = self.review_and_improve_tests(
            #         item, item["source"], test_code
            #     )
            #     self.total_usage = self.provider.update_usage(self.total_usage, usage)
            #     print(f"  ✓ AI tests reviewed and improved successfully")
            #     self.log_step(
            #         "Review and improve AI tests", f"Following improvements requested:\n{requested_improvements}"
            #     )
            #     if len(requested_improvements.get("review_comments", [])) == 0:
            #         print(f"  ✓ Critque is happy with the tests!")
            #         break

                # REGENERATE THE TEST CASES ON FEEDBACK.


            # Step 4: Write test file
            print("• Writing test file...")
            with open(test_file_path, "w") as test_file:
                test_file.write(test_code)
            print(f"  ✓ Test file written successfully")
            self.log_step("Write test file", f"Test file written to: {test_file_path}")

            print("\n✓ Item processing complete")

        print("\nAll items processed successfully!")

    def generate_ai_tests(self, item, source_code, file_extension):
        language_prompts = {
            "py": PYTHON_UNIT_TEST_PROMPT,
            "js": JAVASCRIPT_UNIT_TEST_PROMPT,
            "ts": JAVASCRIPT_UNIT_TEST_PROMPT,
            "jsx": REACT_UNIT_TEST_PROMPT,
            "tsx": REACT_UNIT_TEST_PROMPT,
            "rs": RUST_UNIT_TEST_PROMPT,
        }

        prompt_template = language_prompts.get(
            file_extension, UNIT_TEST_PLAN_PROMPT
        )

        # First, generate test scenarios
        analysis_prompt = UNIT_TEST_PLAN_PROMPT.format(
            SOURCE_CODE=source_code, NODE_TYPE=item["type"], NODE_NAME=item["name"]
        )
        analysis_response, usage = self.provider.chat_completion_with_json(
            analysis_prompt, model="best"
        )
        self.total_usage = self.provider.update_usage(self.total_usage, usage)

        # Format the test scenarios
        test_scenarios = self.format_test_scenarios(analysis_response)

        # Now, generate the actual tests
        prompt = prompt_template.format(
            SOURCE_CODE=source_code,
            NODE_TYPE=item["type"],
            NODE_NAME=item["name"],
            FULL_FILE_PATH=item["full_path"],
            TEST_SCENARIOS=test_scenarios,
        )
        response, usage = self.provider.chat_completion_with_retry(prompt, model="best")
        self.total_usage = self.provider.update_usage(self.total_usage, usage)

        return response, usage

    def review_tests(self, item, source_code, generated_tests):
        prompt = REVIEW_UNIT_TEST_PROMPT.format(
            NODE_TYPE=item["type"],
            NODE_NAME=item["name"],
            CURRENT_TEST=generated_tests,
            SOURCE_CODE=source_code,
        )
        response, usage = self.provider.chat_completion_with_json(prompt, model="best")
        return response, usage

    def generate_tests_with_feedback(self, file_name, test_code):
        file_content_prompt = REVIEW_TEST_CASE_PROMPT.format(
            FILE_NAME=file_name, CODE=test_code
        )
        response, usage = self.provider.chat_completion(
            file_content_prompt, model="best"
        )
        return response, usage

    def _create_output_folder(self, folder_name):
        os.makedirs(folder_name, exist_ok=True)

    def run_tests(self):
        runner = UnitTestRunner(self.output_folder)
        results = runner.discover_and_run_tests()
        return results

    def format_test_scenarios(self, scenarios):
        formatted_scenarios = ""
        for category in [
            "normal_cases",
            "edge_cases",
            "error_handling",
            "boundary_conditions",
        ]:
            cases = scenarios.get(category, [])
            if cases:
                formatted_scenarios += f"{category.replace('_', ' ').title()}:\n"
                for case in cases:
                    formatted_scenarios += f"- {case}\n"
                formatted_scenarios += "\n"
        return formatted_scenarios.strip()

    def log_step(self, step_name, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] Step: {step_name}\n{data}\n{'='*50}\n"

        log_file = os.path.join(self.log_dir, f"unit_test_generator_steps.log")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        with open(log_file, "a") as f:
            f.write(log_message)

        if self.verbose:
            print(f"Logged step: {step_name}")
