import logging
import os
from typing import Optional
from kaizen.helpers import output
from kaizen.llms.provider import LLMProvider
from kaizen.actors.e2e_test_runner import E2ETestRunner
from kaizen.llms.prompts.e2e_tests_prompts import (
    E2E_MODULES_PROMPT,
    E2E_TESTS_SYSTEM_PROMPT,
    PLAYWRIGHT_CODE_PROMPT,
    PLAYWRIGHT_CODE_PLAN_PROMPT,
)
from tqdm import tqdm
import json


class E2ETestGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=E2E_TESTS_SYSTEM_PROMPT)
        self.custom_model = None
        self.test_folder_path = ".kaizen/e2e-tests"
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        if self.provider.models and "best" in self.provider.models:
            self.custom_model = self.provider.models["best"]
            if "type" in self.custom_model:
                del self.custom_model["type"]

    def generate_e2e_tests(
        self,
        web_url: str,
        folder_path: Optional[str] = "",
    ):
        """
        This method generates e2e tests with cypress code for a given web URL.
        """
        web_content = self.extract_webpage(web_url)
        test_modules = self.identify_modules(web_content)
        ui_tests, usage = self.generate_module_tests(
            web_content, test_modules["modules"], web_url
        )
        self.store_tests_files(ui_tests, folder_path)
        self.total_usage = self.provider.update_usage(usage, test_modules["usage"])
        return ui_tests, self.total_usage

    def extract_webpage(self, web_url: str):
        """
        This method extracts the code for a given web URL.
        """

        html = output.get_web_html(web_url)
        self.logger.info(f"Extracted HTML data for {web_url}")
        return html

    def identify_modules(self, web_content: str, user: Optional[str] = None):
        """
        This method identifies the different UI modules from a webpage.
        """
        prompt = E2E_MODULES_PROMPT.format(WEB_CONTENT=web_content)
        resp, usage = self.provider.chat_completion_with_json(
            prompt, user=user, custom_model=self.custom_model
        )
        modules = resp["tests"]
        self.logger.info(f"Extracted modules")
        return {"modules": modules, "usage": usage}

    def generate_playwright_code(
        self,
        web_content: str,
        test_description: str,
        web_url: str,
        user: Optional[str] = None,
    ):
        """
        This method generates playwright code for a particular E2E test.
        """
        code_gen_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        # First generate a plan for code
        prompt = PLAYWRIGHT_CODE_PLAN_PROMPT.format(
            WEB_CONTENT=web_content, TEST_DESCRIPTION=test_description, URL=web_url
        )
        plan, usage = self.provider.chat_completion_with_retry(
            prompt, user=user, custom_model=self.custom_model
        )
        code_gen_usage = self.provider.update_usage(code_gen_usage, usage)

        # Next generate the code based on plan
        code_prompt = PLAYWRIGHT_CODE_PROMPT.format(PLAN_TEXT=plan)
        code, usage = self.provider.chat_completion_with_retry(
            code_prompt, user=user, custom_model=self.custom_model
        )
        code_gen_usage = self.provider.update_usage(code_gen_usage, usage)

        return {"code": code, "usage": code_gen_usage}

    def generate_module_tests(self, web_content: str, test_modules: dict, web_url: str):
        """
        This method generates UI testing points for all modules.
        """
        ui_tests = test_modules
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        for module in tqdm(ui_tests, desc="Processing Modules", unit="module"):
            module_title = module.get(
                "module_title", "Unknown Module"
            )  # Adjust if your module structure is different
            print(f"\n{'=' * 50}")
            print(f"Processing Module: {module_title}")
            print(f"{'=' * 50}")

            # Inner loop
            for i, test in enumerate(module["tests"], 1):
                test_description = test["test_description"]
                print(f"\n--- Test {i}: {test_description} ---")

                print("  • Generating playwright code...")
                playwright_code = self.generate_playwright_code(
                    web_content, test_description, web_url
                )

                print("  • Updating test code...")
                test["code"] = playwright_code["code"]
                test["status"] = "Not run"

                print("  • Updating usage statistics...")
                self.total_usage = self.provider.update_usage(
                    self.total_usage, playwright_code["usage"]
                )

                print("  ✓ Test processing complete")

        print("\nAll modules processed successfully!")

        return ui_tests, self.total_usage

    def store_tests_files(self, json_tests: list, folder_path: str = ""):

        if not folder_path:
            folder_path = output.get_parent_folder()

        folder_path = os.path.join(folder_path, self.test_folder_path)
        output.create_folder(folder_path)
        output.create_test_files(json_tests, folder_path)
        self.logger.info("Successfully store the files")

    def store_module_files(self, module_data: list, folder_path: str = ""):

        if not folder_path:
            folder_path = output.get_parent_folder()

        folder_path = os.path.join(folder_path, self.test_folder_path)
        output.create_folder(folder_path)
        with open(f"{folder_path}/module_info.json", "w+") as f:
            f.write(json.dumps(module_data))

    def run_tests(self):
        """
        This method runs playwright tests and updates logs and status accordingly.
        """
        runner = E2ETestRunner()
        results = runner.run_tests()
        return results
