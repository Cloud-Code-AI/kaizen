import logging
import subprocess
import os
from typing import Optional
import json
from kaizen.helpers import output, parser, general
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts import (
    UI_MODULES_PROMPT,
    UI_TESTS_SYSTEM_PROMPT,
    PLAYWRIGHT_CODE_PROMPT,
)


class UITestGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=UI_TESTS_SYSTEM_PROMPT)

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
        ui_tests = self.generate_module_tests(web_content, test_modules, web_url)
        self.store_tests_files(ui_tests, folder_path)

        return ui_tests

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
        resp = self.provider.chat_completion(prompt, user=user)
        modules = parser.extract_multi_json(resp)
        return modules

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
        prompt = PLAYWRIGHT_CODE_PROMPT.format(
            WEB_CONTENT=web_content, TEST_DESCRIPTION=test_description, URL=web_url
        )

        resp = self.provider.chat_completion(prompt, user=user)

        return resp

    def generate_module_tests(self, web_content: str, test_modules: dict, web_url: str):
        """
        This method generates UI testing points for all modules.
        """
        ui_tests = test_modules
        for module in ui_tests:
            for test in module["tests"]:
                test_description = test["test_description"]
                playwright_code = self.generate_playwright_code(
                    web_content, test_description, web_url
                )
                test["code"] = playwright_code
                test["status"] = "Not run"

        return ui_tests

    def store_tests_files(self, json_tests: list, folder_path: str = ""):
        if not folder_path:
            folder_path = output.get_parent_folder()

        folder_path = os.path.join(folder_path, ".kaizen/tests")
        output.create_folder(folder_path)
        with open(f"{folder_path}/tests.json", "w") as f:
            f.write(json.dumps(json_tests))
        for module in json_tests:
            temp_folder_path = os.path.join(folder_path, module["folder_name"])
            output.create_folder(temp_folder_path)
            for test in module["tests"]:
                file_path = os.path.join(
                    temp_folder_path,
                    "test_" + "_".join(test["test_name"].lower().split(" ")) + ".py",
                )
                with open(file_path, "w") as f:
                    cleaned_code = general.clean_python_code(test["code"])
                    if not cleaned_code:
                        self.logger.info(f"Failed to clean code")
                    else:
                        cleaned_code = (
                            f"''' Module Name: {module['module_title']}\n '''\n\n"
                            + cleaned_code
                        )
                        f.write(cleaned_code)

    def run_tests(self, ui_tests: dict):
        """
        This method runs playwright tests and updates logs and status accordingly.
        """
        subprocess.run(["playwright", "install", "--with-deps"], check=True)
        test_result = ui_tests
        for module in test_result:
            for test in module["tests"]:
                test["logs"], test["status"] = general.run_test(test["code"])

        return test_result
