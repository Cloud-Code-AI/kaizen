import subprocess
import json
import os
import re
import time
from functools import wraps
from pathlib import Path


def safe_path_join(base_path, *paths):
    """
    Safely join two or more pathname components.

    Args:
    base_path (str): The base path.
    *paths (str): Additional path components to join.

    Returns:
    Path: The safely joined path.

    Raises:
    ValueError: If the resulting path would be outside the base path.
    """
    base = Path(base_path).resolve()
    full_path = (base.joinpath(*paths)).resolve()

    if base not in full_path.parents:
        raise ValueError("Resulting path would be outside the base path.")

    return full_path


def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    print(
                        f"Attempt {attempts} failed: error |{e}|. Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)

        return wrapper

    return decorator


def run_test(code):

    # TODO: Update logic for pytest runner

    pass


def clean_python_code(code):
    match = re.search(r"```(?:python)?\n(.*)\n```", code, re.DOTALL)
    if match:
        return match.group(1)
    return None


def create_test_spec(code, path):
    with open(path, "w+") as test_file:
        match = re.search(r"```(?:javascript)?\n(.*)\n```", code, re.DOTALL)

    if match:
        test_code = match.group(1)
        with open(path, "w+") as test_file:
            test_file.write(test_code)


def run_test_script():
    output = subprocess.run(
        ["npx", "playwright", "test"],
        cwd="cloudcode/playwright",
        capture_output=True,
        text=True,
    )
    result = json.loads(output.stdout)
    return result


def extract_result(result_json):
    logs = []
    test_result = "Success"

    for suite in result_json["suites"]:
        if suite["file"] == "temp.spec.js":
            for _, spec in enumerate(suite["specs"]):
                if spec["ok"] is False:
                    test_status = "Failed"
                    test_result = "Failed"
                else:
                    test_status = "Success"

                logs.append(
                    f'Test for {spec["tests"][0]["projectName"]} - {test_status}'
                )

    return logs, test_result


def delete_test_spec(path):
    if os.path.exists(path):
        os.remove(path)
