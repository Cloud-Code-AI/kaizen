import os
import re
import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import glob
import pytest
import io
import sys


class UnitTestRunner:
    def __init__(self, test_directory="./.kaizen/unit_test/"):
        self.test_directory = test_directory
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.supported_extensions = {
            "py": self.run_python_tests,
            "js": self.run_javascript_tests,
            "ts": self.run_typescript_tests,
            "jsx": self.run_react_tests,
            "tsx": self.run_react_ts_tests,
            "rs": self.run_rust_tests,
        }
        self.project_root = None

    @lru_cache(maxsize=None)
    def find_project_root(self, file_path):
        current_dir = os.path.dirname(os.path.abspath(file_path))
        while current_dir != "/":
            if any(
                os.path.exists(os.path.join(current_dir, marker))
                for marker in [
                    "package.json",
                    "Cargo.toml",
                    "pytest.ini",
                    "setup.py",
                    "setup.cfg",
                    "tox.ini",
                    "pyproject.toml",
                ]
            ):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        return None

    def run_command(self, command, cwd=None):
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=cwd,
                shell=False,
                timeout=300,
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 124, "", f"Command timed out after 300 seconds"
        except Exception as e:
            return 1, "", f"Error running command: {str(e)}"

    def discover_and_run_tests(self, test_file=None):
        self.project_root = self.find_project_root(self.test_directory)
        if not self.project_root:
            return {"error": "Could not find project root"}

        test_files = self._discover_test_files(test_file)
        return self._run_tests_in_parallel(test_files)

    def _discover_test_files(self, test_file):
        pattern = os.path.join(
            self.test_directory, "**", f"test_*.{'py' if test_file else '*'}"
        )
        return [
            f
            for f in glob.glob(pattern, recursive=True)
            if f.split(".")[-1] in self.supported_extensions
        ]

    def _run_tests_in_parallel(self, test_files):
        results = {}
        with ThreadPoolExecutor() as executor:
            future_to_file = {
                executor.submit(self._run_test, file): file for file in test_files
            }
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                results[file] = future.result()
        return results

    def _run_test(self, file_path):
        extension = file_path.split(".")[-1]
        return self.supported_extensions[extension](file_path)

    def run_python_tests(self, file_path):
        relative_path = os.path.relpath(file_path, self.project_root)

        captured_output = io.StringIO()
        sys.stdout = captured_output
        sys.stderr = captured_output

        pytest_args = [relative_path, "-v"]
        result = pytest.main(pytest_args)

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        output = captured_output.getvalue()
        return self._parse_pytest_output(output, result)

    def _parse_pytest_output(self, output, result):
        passed_tests = re.findall(r"(.*?) PASSED", output)
        failed_tests = re.findall(r"(.*?) FAILED", output)
        error_tests = re.findall(r"(.*?) ERROR", output)
        tests_run = len(passed_tests) + len(failed_tests) + len(error_tests)

        failure_details = {}
        for match in re.findall(
            r"FAILED (.*?) - Failed:(.*?)(?:\n|$)", output, re.MULTILINE
        ):
            test_path, reason = match
            file_name = test_path.split("::")[0]
            test_name = test_path.split("::")[-1]
            failure_details[file_name] = failure_details.get(file_name, {})
            failure_details[file_name][test_name] = reason.strip()

        error_details = re.findall(r"_{20,}\n(.*?)\n\n", output, re.DOTALL)

        return {
            "tests_run": tests_run,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "error_tests": error_tests,
            "failure_details": failure_details,
            "error_details": error_details,
        }

    def run_javascript_tests(self, file_path):
        relative_path = os.path.relpath(file_path, self.project_root)
        code, stdout, stderr = self.run_command(
            ["npx", "jest", relative_path], cwd=self.project_root
        )
        return self._parse_jest_output(stdout, stderr, code)

    def _parse_jest_output(self, stdout, stderr, code):
        tests_run = stdout.count("PASS") + stdout.count("FAIL")
        failures = stdout.count("FAIL")
        errors = stderr.count("ERROR")

        failure_details = re.findall(r"● (.*?)\n\n", stdout, re.DOTALL)
        error_details = re.findall(r"ERROR.*?\n(.*?)\n\n", stderr, re.DOTALL)

        return {
            "tests_run": tests_run,
            "failures": failures,
            "errors": errors,
            "failure_details": failure_details,
            "error_details": error_details,
        }

    def run_typescript_tests(self, file_path):
        return self.run_javascript_tests(file_path)

    def run_react_tests(self, file_path):
        return self.run_javascript_tests(file_path)

    def run_react_ts_tests(self, file_path):
        return self.run_javascript_tests(file_path)

    def run_rust_tests(self, file_path):
        # relative_path = os.path.relpath(file_path, self.project_root)
        code, stdout, stderr = self.run_command(
            ["cargo", "test", "--", "--nocapture"], cwd=self.project_root
        )
        return self._parse_rust_output(stdout, stderr, code)

    def _parse_rust_output(self, stdout, stderr, code):
        tests_run = stdout.count("test result:")
        failures = stdout.count("FAILED")
        errors = stderr.count("error:")

        failure_details = re.findall(
            r"---- .*? ----\n.*?\n\nthread.*?panicked.*?\n(.*?)\n\n", stdout, re.DOTALL
        )
        error_details = re.findall(r"error:.*?\n(.*?)\n\n", stderr, re.DOTALL)

        return {
            "tests_run": tests_run,
            "failures": failures,
            "errors": errors,
            "failure_details": failure_details,
            "error_details": error_details,
        }
