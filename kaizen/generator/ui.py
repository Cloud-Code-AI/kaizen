import logging
import os
from typing import Optional
from kaizen.helpers import output, parser
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.ui_tests_prompts import (
    UI_MODULES_PROMPT,
    UI_TESTS_SYSTEM_PROMPT,
    PLAYWRIGHT_CODE_PROMPT,
    PLAYWRIGHT_CODE_PLAN_PROMPT,
)


class UITestGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=UI_TESTS_SYSTEM_PROMPT)
        self.custom_model = None
        if self.provider.models and "best" in self.provider.models:
            self.custom_model = self.provider.models["best"]
            if "type" in self.custom_model:
                del self.custom_model["type"]

    def generate_ui_tests(
        self,
        web_url: str,
        folder_path: Optional[str] = "",
    ):
        """
        This method generates UI tests with cypress code for a given web URL.
        """
        web_content = self.extract_webpage(web_url)
        test_modules = self.identify_modules(web_content)
        ui_tests, usage = self.generate_module_tests(
            web_content, test_modules["modules"], web_url
        )
        self.store_tests_files(ui_tests, folder_path)
        total_usage = self.provider.update_usage(usage, test_modules["usage"])
        return ui_tests, total_usage

    def extract_webpage(self, web_url: str):
        """
        This method extracts the code for a given web URL.
        """

        html = output.get_web_html(web_url)
        return html

    def identify_modules(self, web_content: str, user: Optional[str] = None):
        """
        This method identifies the different UI modules from a webpage.
        """
        prompt = UI_MODULES_PROMPT.format(WEB_CONTENT=web_content)
        resp, usage = self.provider.chat_completion(
            prompt, user=user, custom_model=self.custom_model
        )
        modules = parser.extract_multi_json(resp)
        return {"modules": modules, "usage": usage}

    def generate_playwright_code(
        self,
        web_content: str,
        test_description: str,
        web_url: str,
        user: Optional[str] = None,
    ):
        """
        This method generates playwright code for a particular UI test.
        """
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        # First generate a plan for code
        prompt = PLAYWRIGHT_CODE_PLAN_PROMPT.format(
            WEB_CONTENT=web_content, TEST_DESCRIPTION=test_description, URL=web_url
        )
        plan, usage = self.provider.chat_completion(
            prompt, user=user, custom_model=self.custom_model
        )
        total_usage = self.provider.update_usage(total_usage, usage)

        # Next generate the code based on plan
        code_prompt = PLAYWRIGHT_CODE_PROMPT.format(PLAN_TEXT=plan)
        code, usage = self.provider.chat_completion(
            code_prompt, user=user, custom_model=self.custom_model
        )
        total_usage = self.provider.update_usage(total_usage, usage)

        return {"code": code, "usage": total_usage}

    def generate_module_tests(self, web_content: str, test_modules: dict, web_url: str):
        """
        This method generates UI testing points for all modules.
        """
        ui_tests = test_modules
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        for module in ui_tests:
            for test in module["tests"]:
                test_description = test["test_description"]
                playwright_code = self.generate_playwright_code(
                    web_content, test_description, web_url
                )
                test["code"] = playwright_code["code"]
                test["status"] = "Not run"
                total_usage = self.provider.update_usage(
                    total_usage, playwright_code["usage"]
                )

        return ui_tests, total_usage

    def store_tests_files(self, json_tests: list, folder_path: str = ""):

        if not folder_path:
            folder_path = output.get_parent_folder()

        folder_path = os.path.join(folder_path, ".kaizen/ui-tests")
        output.create_folder(folder_path)
        output.create_test_files(json_tests, folder_path)

    def run_tests(self, ui_tests: dict):
        """
        This method runs playwright tests and updates logs and status accordingly.
        """
        pass
