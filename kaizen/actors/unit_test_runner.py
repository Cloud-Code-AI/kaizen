import subprocess
import os
from kaizen.helpers.general import safe_path_join


class UnitTestRunner:
    def __init__(self, test_directory="./.kaizen/unit_test/"):
        self.test_directory = test_directory
        self.supported_extensions = {
            "py": self.run_python_tests,
            "js": self.run_javascript_tests,
            "ts": self.run_typescript_tests,
            "jsx": self.run_react_tests,
            "tsx": self.run_react_ts_tests,
            "rs": self.run_rust_tests,
        }

    def run_command(self, command, cwd=None):
        try:
            result = subprocess.run(command, capture_output=True, text=True, cwd=cwd)
            return result.returncode, result.stdout, result.stderr
        except FileNotFoundError:
            return 1, "", f"Command not found: {command[0]}"

    def find_project_root(self, file_path):
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
                return current_dir
            current_dir = os.path.dirname(current_dir)
        return None

    def discover_and_run_tests(self):
        results = {}
        for root, dirs, files in os.walk(self.test_directory):
            for file in files:
                if file.startswith("test_"):
                    file_path = safe_path_join(root, file)
                    extension = file.split(".")[-1]
                    if extension in self.supported_extensions:
                        result = self.supported_extensions[extension](file_path)
                        results[file_path] = result
                    else:
                        results[file_path] = {
                            "error": f"Unsupported file type: .{extension}"
                        }
        return results

    def run_python_tests(self, file_path):
        project_root = self.find_project_root(file_path)
        if not project_root:
            return {"error": "Could not find project root (no pytest.ini found)"}

        relative_path = os.path.relpath(file_path, project_root)
        print(relative_path)
        code, stdout, stderr = self.run_command(
            ["pytest", relative_path, "-v"], cwd=project_root
        )

        if (
            code != 0 and code != 1
        ):  # pytest returns 1 if tests fail, but that's not an error for us
            return {"error": f"pytest exited with code {code}. Stderr: {stderr}"}

        # Parse pytest output
        tests_run = stdout.count("PASSED") + stdout.count("FAILED")
        failures = stdout.count("FAILED")
        errors = stderr.count("ERROR")

        return {"tests_run": tests_run, "failures": failures, "errors": errors}

    def run_javascript_tests(self, file_path):
        project_root = self.find_project_root(file_path)
        if not project_root:
            return {"error": "Could not find project root (no package.json found)"}

        relative_path = os.path.relpath(file_path, project_root)
        code, stdout, stderr = self.run_command(
            ["npx", "jest", relative_path], cwd=project_root
        )

        if code != 0:
            return {"error": f"Jest exited with code {code}. Stderr: {stderr}"}

        # Simplified parsing of Jest output
        return {
            "tests_run": stdout.count("PASS") + stdout.count("FAIL"),
            "failures": stdout.count("FAIL"),
            "errors": stderr.count("ERROR"),
        }

    def run_typescript_tests(self, file_path):
        return self.run_javascript_tests(file_path)

    def run_react_tests(self, file_path):
        return self.run_javascript_tests(file_path)

    def run_react_ts_tests(self, file_path):
        return self.run_javascript_tests(file_path)

    def run_rust_tests(self, file_path):
        project_root = self.find_project_root(file_path)
        if not project_root:
            return {"error": "Could not find project root (no Cargo.toml found)"}

        code, stdout, stderr = self.run_command(
            ["cargo", "test", "--", "--nocapture"], cwd=project_root
        )

        if code != 0:
            return {"error": f"Cargo exited with code {code}. Stderr: {stderr}"}

        # Simplified parsing of Cargo test output
        return {
            "tests_run": stdout.count("test result:"),
            "failures": stdout.count("FAILED"),
            "errors": stderr.count("error:"),
        }
