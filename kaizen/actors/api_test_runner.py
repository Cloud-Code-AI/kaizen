import shlex
import os
import re
import subprocess
import logging
from kaizen.helpers.general import safe_path_join


class APITestRunner:
    def __init__(self, test_directory="./.kaizen/api_test/"):
        self.test_directory = test_directory
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(
            f"APITestRunner initialized with test directory: {test_directory}"
        )
    
    def discover_and_run_tests(self, test_file=None):
        if test_file is None:
            self.logger.warning("No test file specified. Running all tests.")
        self.logger.info("Starting test discovery and execution")
        results = {}
        for root, dirs, files in os.walk(self.test_directory):
            for file in files:
                if file.startswith("test_") and file.endswith(".py"):
                    file_path = safe_path_join(root, file)
                    self.logger.debug(f"Found test file: {file_path}")
                    if test_file and file not in test_file:
                        self.logger.debug("Skipping file test")
                        continue

                    self.logger.info(f"Running tests for: {file_path}")
                    result = self.run_python_tests(file_path)
                    results[str(file_path)] = result
        
        self.logger.info("Test discovery and execution completed")
        return results
    
    def run_python_tests(self, file_path):
        self.logger.info(f"Running Python tests for: {file_path}")
        project_root = self.find_project_root(file_path)
        if not project_root:
            self.logger.error("Could not find project root (no pytest.ini found)")
            return {"error": "Could not find project root (no pytest.ini found)"}

        relative_path = os.path.relpath(file_path, project_root)
        code, stdout, stderr = self.run_command(
            ["pytest", relative_path, "-v"], cwd=project_root
        )

        if code != 0 and code != 1:
            self.logger.error(f"pytest exited with code {code} for {file_path}")
            return {"error": f"pytest exited with code {code}. Stderr: {stderr}"}
        self.logger.info(f"pytest output: {stdout}")
        # Parse pytest output

        # Get failed test details
        passed_tests = re.findall(r"(.*?) PASSED", stdout)
        failed_tests = re.findall(r"(.*?) FAILED", stdout)
        error_tests = re.findall(r"(.*?) ERROR", stderr)
        tests_run = len(passed_tests) + len(failed_tests) + len(error_tests)

        # Extract failure and error details
        # Extract failure and error details
        failure_details = {}
        for match in re.findall(
            r"FAILED (.*?) - Failed:(.*?)(?:\n|$)", stdout + stderr, re.MULTILINE
        ):
            test_path, reason = match
            file_name = test_path.split("::")[0]
            test_name = test_path.split("::")[-1]
            failure_details[file_name] = failure_details.get(file_name, {})
            failure_details[file_name][test_name] = reason.strip()

        error_details = re.findall(r"_{20,}\n(.*?)\n\n", stderr, re.DOTALL)

        self.logger.info(
            f"Python tests completed. Tests run: {tests_run}, Failures: {len(failed_tests)}, Errors: {len(error_tests)}"
        )
        return {
            "tests_run": tests_run,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "error_tests": error_tests,
            "failure_details": failure_details,
            "error_details": error_details,
        }

    def find_project_root(self, file_path):
        self.logger.debug(f"Searching for project root from: {file_path}")
        current_dir = os.path.dirname(os.path.abspath(file_path))
        while current_dir != "/":
            if (
                os.path.exists(os.path.join(current_dir, "package.json"))
                or os.path.exists(os.path.join(current_dir, "Cargo.toml"))
                or os.path.exists(os.path.join(current_dir, "pytest.ini"))
                or os.path.exists(os.path.join(current_dir, "setup.py"))
                or os.path.exists(os.path.join(current_dir, "setup.cfg"))
                or os.path.exists(os.path.join(current_dir, "tox.ini"))
                or os.path.exists(os.path.join(current_dir, "pyproject.toml"))
            ):
                self.logger.info(f"Project root found: {current_dir}")
                return current_dir
            current_dir = os.path.dirname(current_dir)
        self.logger.warning("Project root not found")
        return None
    
    def run_command(self, command, cwd=None):
        self.logger.debug(f"Running command: {' '.join(command)} in directory: {cwd}")
        try:
            # Use shlex.split() to properly handle command arguments
            if isinstance(command, str):
                command = shlex.split(command)

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=cwd,
                shell=False,
                timeout=300,
            )
            self.logger.debug(
                f"Command completed with return code: {result.returncode}"
            )
            return result.returncode, result.stdout, result.stderr
        except FileNotFoundError:
            self.logger.error(f"Command not found: {command[0]}")
            return 1, "", f"Command not found: {command[0]}"
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed with return code {e.returncode}: {e}")
            return e.returncode, e.stdout, e.stderr
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out after {self.timeout} seconds")
            return 124, "", f"Command timed out after {self.timeout} seconds"