import subprocess
import json
import os
import re


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
