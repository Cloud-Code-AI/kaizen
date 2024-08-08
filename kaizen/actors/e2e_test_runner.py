import asyncio
import glob
import json
import os
from playwright.async_api import async_playwright


class E2ETestRunner:
    def __init__(self, test_directory="./.kaizen/e2e-tests/"):
        self.test_directory = test_directory

    def run_tests(self):
        """
        This method runs playwright tests and updates logs and status accordingly.
        """

        async def run_test(test):
            async with async_playwright() as p:
                browser = await p.chromium.launch()
                page = await browser.new_page()
                try:
                    await page.goto(test["url"])
                    await page.evaluate(test["code"])
                    test["status"] = "Passed"
                except Exception as e:
                    test["status"] = "Failed"
                    test["error"] = str(e)
                finally:
                    await browser.close()

        tests_dir = self.test_directory
        tests = []
        for test_file in glob.glob(os.path.join(tests_dir, "*.json")):
            with open(test_file, "r") as f:
                tests.extend(json.load(f))

        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(run_test(test)) for test in tests]
        loop.run_until_complete(asyncio.gather(*tasks))
        return tests
