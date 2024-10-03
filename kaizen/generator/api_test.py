import os
import logging
from datetime import datetime
from tqdm import tqdm
import json
from dataclasses import dataclass
from typing import List, Dict
from kaizen.llms.provider import LLMProvider
from kaizen.helpers.parser import extract_code_from_markdown
from kaizen.actors.api_test_runner import APITestRunner
from kaizen.llms.prompts.API_tests_prompts import (
    API_TEST_SYSTEM_PROMPT,
    API_METHOD_PROMPT,
)


@dataclass
class APITestOutput:
    tests: Dict
    files: List
    failed: List
    usage: Dict[str, int]
    model_name: str
    cost: Dict[str, float]


class APITestGenerator:
    def __init__(self, verbose=False):
        self.output_folder = "./.kaizen/api_test/"
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=API_TEST_SYSTEM_PROMPT)
        self.verbose = verbose
        self.log_dir = "./.kaizen/logs"
        self.max_critique = 3
        self.enable_critique = False
        self._setup_directories()

    def _setup_directories(self):
        os.makedirs(self.log_dir, exist_ok=True)
        self._create_output_folder(self.output_folder)

    def _create_output_folder(self, folder_name):
        os.makedirs(folder_name, exist_ok=True)
        print("Output folder created")

    def generate_tests(
        self,
        file_path: str,
        base_url: str,
        content: str = None,
        max_critique: int = 3,
        output_path: str = None,
        verbose: bool = False,
        enable_critique: bool = False,
        temp_dir: str = "",
        max_actions: int = 100000,
    ):
        self.max_critique = max_critique
        self.enable_critique = enable_critique
        self.verbose = verbose if verbose else self.verbose
        self.output_folder = output_path if output_path else self.output_folder
        self.temp_dir = temp_dir
        self.max_actions = max_actions
        self.base_url = base_url if base_url else "https://api.example.com"
        content = content or self._read_file_content(file_path)
        self.generate_test_files(content, file_path)
        return {}, self.total_usage

    def _read_file_content(self, file_path):
        try:
            with open(file_path, "r") as file:
                api_schema = json.load(file)
        except UnicodeDecodeError:
            print(f"Error reading file: {file_path}")
        return api_schema

    def generate_test_files(self, file_data, file_path):
        folder_path = "/".join(file_path.split("/")[:-1])
        test_files = {}
        actions_used = 0
        for path, path_item in tqdm(
            file_data["paths"].items(), desc="Processing Endpoints(Paths)", unit="paths"
        ):
            try:
                test_code, count = self._process_item(path, path_item, folder_path)
                test_files[file_path] = test_code
                actions_used += count
            except Exception as e:
                self.logger.error(
                    f"Failed to generate test case for item: {path}. Error: {str(e)}"
                )
                break

        print(
            f"\nAll items processed successfully!\n Total Tokens Spent: {self.total_usage}"
        )
        return test_files, actions_used

    def _process_item(self, path, path_item, folder_path):
        print(f"\n{'=' * 50}\nProcessing Item: {path}\n{'=' * 50}")
        file_path = path.replace("/", "_").replace("{", "").replace("}", "")
        test_file_path = self._prepare_test_file_path(file_path, folder_path)
        test_code = ""
        totalcount = 0
        for method, method_code in path_item.items():
            print("Processing method:", method)
            individual_test_code, count = self.generate_ai_tests(
                path, method, method_code
            )
            test_code += individual_test_code
            totalcount += count

        test_code = test_code.replace(self.temp_dir, "")
        test_code = self._correct_imports(test_code)

        self._write_test_file(test_file_path, test_code)

        print("\n✓ Item processing complete")
        return test_code, totalcount

    def _prepare_test_file_path(self, path, folder_path):
        print("Preparing test file path")
        test_file_name = f"test_{path.lower()}.py"
        test_file_path = os.path.join(self.output_folder, test_file_name)
        self._create_output_folder("/".join(test_file_path.split("/")[:-1]))
        print(f"  ✓ File will be saved as: {test_file_path}")
        return test_file_path

    def generate_ai_tests(self, path, method, method_code):
        print(f"• Generating AI tests for {method.upper()} {path} ...")
        test_generation_prompt = API_METHOD_PROMPT.format(
            path=path, method=method, method_code=method_code, base_url=self.base_url
        )
        response, usage = self.provider.chat_completion_with_json(
            test_generation_prompt, model="default"
        )
        self.update_usage(usage)
        test_code = extract_code_from_markdown(response)
        print(f"  ✓ AI tests generated successfully for {method.upper()} {path}")
        self.log_step("Generate AI tests", f"Generated test code:\n{response}")
        return test_code, 1

    def run_tests(self, test_file=None):
        runner = APITestRunner(self.output_folder)
        return runner.discover_and_run_tests(test_file=test_file)

    def _correct_imports(self, test_code):
        # Split the test_code into lines
        lines = test_code.split("\n")
        corrected_lines = []
        for line in lines:
            if line.startswith("from /"):
                # Remove the leading slash and change to relative import
                corrected_line = "from " + line[6:]
                corrected_lines.append(corrected_line)
            else:
                corrected_lines.append(line)
        return "\n".join(corrected_lines)

    def format_test_scenarios(self, scenarios):
        count = 0
        formatted_scenarios = ""
        for category in [
            "critical_cases",
            "edge_cases",
            "error_handling",
            "boundary_conditions",
        ]:
            count += 1
            cases = scenarios.get(category, [])
            if cases:
                formatted_scenarios += f"{category.replace('_', ' ').title()}:\n"
                formatted_scenarios += "\n".join(f"- {case}" for case in cases)
                formatted_scenarios += "\n\n"
        return formatted_scenarios.strip(), count

    def log_step(self, step_name, data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] Step: {step_name}\n{data}\n{'=' * 50}\n"

        log_file = os.path.join(self.log_dir, "api_test_generator_steps.log")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        if self.verbose:
            with open(log_file, "a") as f:
                f.write(log_message)
            print(f"Logged step: {step_name}")

    def _write_test_file(self, test_file_path, test_code):
        print("• Writing test file...")
        try:
            with open(test_file_path, "w") as test_file:
                test_file.write(test_code)
            print("  ✓ Test file written successfully")
            self.log_step("Write test file", f"Test file written to: {test_file_path}")
        except Exception as e:
            self.logger.error(f"Failed to write test file. Error: {str(e)}")

    def update_usage(self, usage):
        self.total_usage = self.provider.update_usage(self.total_usage, usage)
        print(f"@ Token usage: current_step: {usage}, total: {self.total_usage}")
