from cloudcode.helpers import output, parser
from typing import Optional
from cloudcode.llms.provider import LLMProvider
from cloudcode.llms.prompts import (
    UI_MODULES_PROMPT,
    UI_TESTS_SYSTEM_PROMPT,
    CYPRESS_CODE_PROMPT
)
import logging


class UITester:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(
            system_prompt=UI_TESTS_SYSTEM_PROMPT,
            max_tokens=15000
        )

    def generate_ui_tests(
        self,
        web_url: str
    ):
        """
        This method generates UI tests with cypress code for a given web URL.
        """
        web_content = self.extract_webpage(web_url)
        test_modules = self.identify_modules(web_content)
        ui_tests = self.generate_module_tests(web_content, test_modules)

        return ui_tests

    def extract_webpage(
        self,
        web_url: str
    ):
        """
        This method extracts the code for a given web URL.
        """

        html = output.get_web_html(web_url)
        return html

    def identify_modules(
        self,
        web_content: str,
        user: Optional[str] = None
    ):
        """
        This method identifies the different UI modules from a webpage.
        """

        prompt = UI_MODULES_PROMPT.format(
            WEB_CONTENT=web_content
        )
        
        resp = self.provider.chat_completion(prompt, user=user)

        modules = parser.extract_json(resp)

        return modules
    
    def generate_cypress_code(
            self,
            web_content: str,
            test_description: str,
            user: Optional[str] = None
    ):
        """
        This method generates cypress code for a particular UI test.
        """
        prompt = CYPRESS_CODE_PROMPT.format(
            WEB_CONTENT=web_content,
            TEST_DESCRIPTION=test_description
        )
            
        resp = self.provider.chat_completion(prompt, user=user)

        return resp

    def generate_module_tests(
        self,
        web_content: str,
        test_modules: dict
    ):
        """
        This method generates UI testing points for all modules.
        """
        ui_tests = test_modules
        for module in ui_tests["modules"]:
            for test in module["tests"]:
                test_description = test["test_description"]
                cypress_code = self.generate_cypress_code(web_content, test_description)
                test["code"] = cypress_code
                test["status"] = "Not run"

        return ui_tests
