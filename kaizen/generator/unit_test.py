import os
import importlib
import logging
from datetime import datetime
from tqdm import tqdm
import json
from pathlib import Path
from kaizen.llms.provider import LLMProvider
from kaizen.helpers.parser import extract_code_from_markdown
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


class UnitTestGenerator:
    SUPPORTED_LANGUAGES = {
        "py": "PythonParser",
        "js": "JavaScriptParser",
        "ts": "TypeScriptParser",
        "jsx": "ReactParser",
        "tsx": "ReactTSParser",
        "rs": "RustParser",
    }

    LANGUAGE_PROMPTS = {
        "py": PYTHON_UNIT_TEST_PROMPT,
        "js": JAVASCRIPT_UNIT_TEST_PROMPT,
        "ts": JAVASCRIPT_UNIT_TEST_PROMPT,
        "jsx": REACT_UNIT_TEST_PROMPT,
        "tsx": REACT_UNIT_TEST_PROMPT,
        "rs": RUST_UNIT_TEST_PROMPT,
    }

    def __init__(self, verbose=False):
        self.output_folder = "./.kaizen/unit_test/"
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=UNIT_TEST_SYSTEM_PROMPT)
        self.verbose = verbose
        self.log_dir = "./.kaizen/logs"
        self.max_critique = 3
        self.enable_critique = False
        self._setup_directories()

    def _setup_directories(self):
        os.makedirs(self.log_dir, exist_ok=True)
        self._create_output_folder(self.output_folder)

    def generate_tests_from_dir(
        self,
        dir_path: str,
        output_path: str = None,
        max_critique: int = 3,
        verbose: bool = False,
        enable_critique: bool = False,
    ):
        """
        dir_path: (str) - path of the directory containing source files
        """
        self.max_critique = max_critique
        self.enable_critique = enable_critique
        self.verbose = verbose if verbose else self.verbose
        self.output_folder = output_path if output_path else self.output_folder
        for file_path in Path(dir_path).rglob("*.*"):
            try:
                self.generate_tests(file_path=str(file_path), output_path=output_path)
            except Exception as e:
                print(f"Error: Could not generate tests for {file_path}: {e}")

        return {}, self.total_usage

    def generate_tests(
        self,
        file_path: str,
        content: str = None,
        max_critique: int = 3,
        output_path: str = None,
        verbose: bool = False,
        enable_critique: bool = False,
    ):
        self.max_critique = max_critique
        self.enable_critique = enable_critique
        self.verbose = verbose if verbose else self.verbose
        self.output_folder = output_path if output_path else self.output_folder

        file_extension = file_path.split(".")[-1]
        if file_extension not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported file type: .{file_extension}")

        parser = self._get_parser(file_extension)
        content = content or self._read_file_content(file_path)
        parsed_data = parser.parse(content)

        self.generate_test_files(parsed_data, file_extension, file_path)
        return {}, self.total_usage

    def _get_parser(self, file_extension):
        parser_class_name = self.SUPPORTED_LANGUAGES[file_extension]
        parser_module = importlib.import_module(
            f"kaizen.parsers.{parser_class_name.lower()}"
        )
        parser_class = getattr(parser_module, parser_class_name)
        return parser_class()

    def _read_file_content(self, file_path):
        with open(file_path, "r") as file:
            return file.read()

    def generate_test_files(self, parsed_data, file_extension, file_path):
        folder_path = "/".join(file_path.split("/")[:-1])
        self.total_usage = self.provider.DEFAULT_USAGE

        for item in tqdm(parsed_data, desc="Processing Items", unit="item"):
            try:
                self._process_item(item, file_extension, file_path, folder_path)
            except Exception:
                self.logger.error(f"Failed to generate test case for item: {item}")

        print(
            f"\nAll items processed successfully!\n Total Tokens Spent: {self.total_usage}"
        )
        self.total_usage = self.provider.DEFAULT_USAGE

    def _process_item(self, item, file_extension, file_path, folder_path):
        print(f"\n{'='*50}\nProcessing Item: {item['name']}\n{'='*50}")

        test_file_path = self._prepare_test_file_path(item, file_extension, folder_path)
        item["full_path"] = file_path

        test_code = self.generate_ai_tests(item, item["source"], file_extension)

        self._write_test_file(test_file_path, test_code)

        print("\n✓ Item processing complete")

    def _prepare_test_file_path(self, item, file_extension, folder_path):
        test_file_name = f"test_{item['name'].lower()}.{file_extension}"
        test_file_path = os.path.join(self.output_folder, folder_path, test_file_name)
        self._create_output_folder("/".join(test_file_path.split("/")[:-1]))
        print(f"  ✓ File will be saved as: {test_file_path}")
        return test_file_path

    def generate_ai_tests(self, item, source_code, file_extension):
        prompt_template = self.LANGUAGE_PROMPTS.get(
            file_extension, UNIT_TEST_PLAN_PROMPT
        )
        print("• Creating a Plan for tests ...")
        plan_response, usage = self._generate_test_scenarios(item, source_code)
        self.update_usage(usage)
        print("  ✓ Plan Created successfully ...")
        self.log_step(
            "Generated Test Scenario", f"Generated Test Scenario:\n{plan_response}"
        )
        test_scenarios = self.format_test_scenarios(plan_response)
        print("• Generating AI tests...")

        response, usage = self._generate_actual_tests(
            item, source_code, test_scenarios, prompt_template
        )
        self.update_usage(usage)
        test_code = extract_code_from_markdown(response)
        print(f"  ✓ AI tests generated successfully")
        self.log_step("Generate AI tests", f"Generated test code:\n{response}")
        if self.enable_critique:
            test_code = self._review_tests_by_critique(item, source_code, test_code)

        return test_code

    def _generate_test_scenarios(self, item, source_code):
        analysis_prompt = UNIT_TEST_PLAN_PROMPT.format(
            SOURCE_CODE=source_code, NODE_TYPE=item["type"], NODE_NAME=item["name"]
        )
        return self.provider.chat_completion_with_json(analysis_prompt, model="best")

    def _review_tests_by_critique(self, item, source_code, test_code):
        """Generates reviews and regenerates tests based on feedbacks."""
        print(f"\t• Using Actor Critique method with {self.max_critique} tries...")
        review, usage = self.review_tests(item, source_code, test_code)
        self.update_usage(usage)
        counter = 1
        feedbacks = review.get("review_comments", [])
        self.log_step(f"- Critique Attempt: {counter}", f" Feedbacks: {feedbacks}")
        print(f"\t\t - Critique Attempt: {counter}: Feedbacks: {len(feedbacks)}")
        while counter < self.max_critique:
            response, usage = self.generate_tests_with_feedback(test_code, feedbacks)
            test_code = extract_code_from_markdown(response)
            self.update_usage(usage)
            counter += 1
            # Perform Review again
            review, usage = self.review_tests(item, source_code, test_code)
            self.update_usage(usage)
            feedbacks = review.get("review_comments", [])
            self.log_step(
                f"- Critique Attempt: {counter}", f"Generated TEst Code:\n {test_code}"
            )
            self.log_step(f"- Critique Attempt: {counter}", f" Feedbacks: {feedbacks}")
            print(f"\t\t - Critique Attempt: {counter}: Feedbacks: {len(feedbacks)}")
            if len(feedbacks) == 0:
                # Critique is satisfied, stop the loop
                print("\t\t ✓ Critique completed as no feedbacks")
                break
        print(f"\t✓ Critique completed")
        return test_code

    def _generate_actual_tests(
        self, item, source_code, test_scenarios, prompt_template
    ):
        prompt = prompt_template.format(
            SOURCE_CODE=source_code,
            NODE_TYPE=item["type"],
            NODE_NAME=item["name"],
            FULL_FILE_PATH=item["full_path"],
            TEST_SCENARIOS=test_scenarios,
        )
        return self.provider.chat_completion_with_retry(prompt, model="best")

    def review_tests(self, item, source_code, generated_tests):
        prompt = REVIEW_UNIT_TEST_PROMPT.format(
            NODE_TYPE=item["type"],
            NODE_NAME=item["name"],
            CURRENT_TEST=generated_tests,
            SOURCE_CODE=source_code,
        )
        return self.provider.chat_completion_with_json(prompt, model="best")

    def generate_tests_with_feedback(self, test_code, feedback):
        file_content_prompt = REVIEW_TEST_CASE_PROMPT.format(
            CODE=test_code, FEEDBACKS=json.dumps(feedback)
        )
        return self.provider.chat_completion(file_content_prompt, model="best")

    def _create_output_folder(self, folder_name):
        os.makedirs(folder_name, exist_ok=True)

    def run_tests(self):
        runner = UnitTestRunner(self.output_folder)
        return runner.discover_and_run_tests()

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
                formatted_scenarios += "\n".join(f"- {case}" for case in cases)
                formatted_scenarios += "\n\n"
        return formatted_scenarios.strip()

    def log_step(self, step_name, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] Step: {step_name}\n{data}\n{'='*50}\n"

        log_file = os.path.join(self.log_dir, "unit_test_generator_steps.log")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        if self.verbose:
            with open(log_file, "a") as f:
                f.write(log_message)
            print(f"Logged step: {step_name}")

    def _write_test_file(self, test_file_path, test_code):
        print("• Writing test file...")
        with open(test_file_path, "w") as test_file:
            test_file.write(test_code)
        print(f"  ✓ Test file written successfully")
        self.log_step("Write test file", f"Test file written to: {test_file_path}")

    def update_usage(self, usage):
        self.total_usage = self.provider.update_usage(self.total_usage, usage)
        print(f"@ Token usage: current_step: {usage}, total: {self.total_usage}")
