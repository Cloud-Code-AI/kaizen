from cloudcode.helpers import parser
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
        self.provider = LLMProvider(system_prompt=UI_TESTS_SYSTEM_PROMPT)

    def generate_ui_tests(
        self,
        web_url: str
    ):
        """
        This method generates UI testswith cypress code for a given web URL.
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

        # TODO: Update extraction logic

        html = """
        <!--
            This example requires some changes to your config:

            ```
            // tailwind.config.js
            module.exports = {
                // ...
                plugins: [
                // ...
                require('@tailwindcss/forms'),
                ],
            }
            ```
            -->
            <!--
            This example requires updating your template:

            ```
            <html class="h-full bg-white">
            <body class="h-full">
            ```
            -->
            <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
            <div class="sm:mx-auto sm:w-full sm:max-w-sm">
                <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company">
                <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
            </div>

            <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                <form class="space-y-6" action="#" method="POST">
                <div>
                    <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email address</label>
                    <div class="mt-2">
                    <input id="email" name="email" type="email" autocomplete="email" required class="block w-full rounded-md border-0 py-1.5 text-gray-900
                    shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600
                    sm:text-sm sm:leading-6">
                    </div>
                </div>

                <div>
                    <div class="flex items-center justify-between">
                    <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
                    <div class="text-sm">
                        <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">Forgot password?</a>
                    </div>
                    </div>
                    <div class="mt-2">
                    <input id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md
                    border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset
                    focus:ring-indigo-600 sm:text-sm sm:leading-6">
                    </div>
                </div>

                <div>
                    <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6
                    text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2
                    focus-visible:outline-indigo-600">Sign in</button>
                </div>
                </form>

                <p class="mt-10 text-center text-sm text-gray-500">
                Not a member?
                <a href="#" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Start a 14 day free trial</a>
                </p>
            </div>
            </div>
        """
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
