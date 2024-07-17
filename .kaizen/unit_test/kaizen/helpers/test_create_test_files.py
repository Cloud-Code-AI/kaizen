import os
import json
from unittest import mock
from kaizen.helpers.output import create_test_files


@mock.patch(
    "kaizen.helpers.output.os.path.join", side_effect=lambda *args: "/".join(args)
)
@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch(
    "kaizen.helpers.output.general.clean_python_code", side_effect=lambda code: code
)
@mock.patch("kaizen.helpers.output.logger.info")
def test_create_test_files_normal_case(
    mock_logger_info,
    mock_clean_python_code,
    mock_create_folder,
    mock_path_join,
    tmp_path,
):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test One",
                    "test_description": "Description of Test One",
                    "code": 'print("Hello World")',
                }
            ],
        }
    ]
    folder_path = str(tmp_path)

    create_test_files(json_tests, folder_path)

    # Check if the tests.json file is created
    with open(os.path.join(folder_path, "tests.json"), "r") as f:
        data = json.load(f)
        assert data == json_tests

    # Check if the test file is created with the correct content
    test_file_path = os.path.join(folder_path, "module1", "test_test_one.py")
    with open(test_file_path, "r") as f:
        content = f.read()
        expected_content = """'''Importance: High\nModule Name: Module 1\nDescription: Description of Test One\n'''

print("Hello World")"""
        assert content == expected_content


@mock.patch(
    "kaizen.helpers.output.os.path.join", side_effect=lambda *args: "/".join(args)
)
@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch(
    "kaizen.helpers.output.general.clean_python_code", side_effect=lambda code: ""
)
@mock.patch("kaizen.helpers.output.logger.info")
def test_create_test_files_failed_clean_code(
    mock_logger_info,
    mock_clean_python_code,
    mock_create_folder,
    mock_path_join,
    tmp_path,
):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test One",
                    "test_description": "Description of Test One",
                    "code": 'print("Hello World")',
                }
            ],
        }
    ]
    folder_path = str(tmp_path)

    create_test_files(json_tests, folder_path)

    # Check if the tests.json file is created
    with open(os.path.join(folder_path, "tests.json"), "r") as f:
        data = json.load(f)
        assert data == json_tests

    # Check if the logger.info was called due to failed clean code
    mock_logger_info.assert_called_with("Failed to clean code")


@mock.patch(
    "kaizen.helpers.output.os.path.join", side_effect=lambda *args: "/".join(args)
)
@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch(
    "kaizen.helpers.output.general.clean_python_code", side_effect=lambda code: code
)
@mock.patch("kaizen.helpers.output.logger.info")
def test_create_test_files_empty_tests(
    mock_logger_info,
    mock_clean_python_code,
    mock_create_folder,
    mock_path_join,
    tmp_path,
):
    json_tests = []
    folder_path = str(tmp_path)

    create_test_files(json_tests, folder_path)

    # Check if the tests.json file is created
    with open(os.path.join(folder_path, "tests.json"), "r") as f:
        data = json.load(f)
        assert data == json_tests

    # Check that no folders or test files are created
    assert len(os.listdir(folder_path)) == 1  # Only tests.json should be present


@mock.patch(
    "kaizen.helpers.output.os.path.join", side_effect=lambda *args: "/".join(args)
)
@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch(
    "kaizen.helpers.output.general.clean_python_code", side_effect=lambda code: code
)
@mock.patch("kaizen.helpers.output.logger.info")
def test_create_test_files_special_characters_in_test_name(
    mock_logger_info,
    mock_clean_python_code,
    mock_create_folder,
    mock_path_join,
    tmp_path,
):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test@One!",
                    "test_description": "Description of Test One",
                    "code": 'print("Hello World")',
                }
            ],
        }
    ]
    folder_path = str(tmp_path)

    create_test_files(json_tests, folder_path)

    # Check if the tests.json file is created
    with open(os.path.join(folder_path, "tests.json"), "r") as f:
        data = json.load(f)
        assert data == json_tests

    # Check if the test file is created with the correct content
    test_file_path = os.path.join(folder_path, "module1", "test_test@one!.py")
    with open(test_file_path, "r") as f:
        content = f.read()
        expected_content = """'''Importance: High\nModule Name: Module 1\nDescription: Description of Test One\n'''

print("Hello World")"""
        assert content == expected_content
