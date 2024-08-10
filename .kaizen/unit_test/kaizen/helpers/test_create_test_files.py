import os
import json
from unittest import mock
from kaizen.helpers.output import create_test_files


@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch("kaizen.helpers.output.general.clean_python_code")
@mock.patch("kaizen.helpers.output.logger")
def test_create_test_files_normal_case(
    mock_logger, mock_clean_python_code, mock_create_folder
):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "high",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test Case 1",
                    "test_description": "Description 1",
                    "code": "print('Hello World')",
                }
            ],
        }
    ]
    folder_path = "test_folder"
    mock_clean_python_code.return_value = "print('Hello World')"

    create_test_files(json_tests, folder_path)

    mock_create_folder.assert_called_once_with(os.path.join(folder_path, "module1"))
    mock_clean_python_code.assert_called_once_with("print('Hello World')")
    mock_logger.info.assert_not_called()

    with open(os.path.join(folder_path, "tests.json"), "r") as f:
        assert json.load(f) == json_tests

    with open(os.path.join(folder_path, "module1", "test_test_case_1.py"), "r") as f:
        content = f.read()
        assert "Importance: high" in content
        assert "Module Name: Module 1" in content
        assert "Description: Description 1" in content
        assert "print('Hello World')" in content


@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch("kaizen.helpers.output.general.clean_python_code")
@mock.patch("kaizen.helpers.output.logger")
def test_create_test_files_empty_code(
    mock_logger, mock_clean_python_code, mock_create_folder
):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "high",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test Case 1",
                    "test_description": "Description 1",
                    "code": "print('Hello World')",
                }
            ],
        }
    ]
    folder_path = "test_folder"
    mock_clean_python_code.return_value = ""

    create_test_files(json_tests, folder_path)

    mock_create_folder.assert_called_once_with(os.path.join(folder_path, "module1"))
    mock_clean_python_code.assert_called_once_with("print('Hello World')")
    mock_logger.info.assert_called_once_with("Failed to clean code")

    with open(os.path.join(folder_path, "tests.json"), "r") as f:
        assert json.load(f) == json_tests

    assert not os.path.exists(
        os.path.join(folder_path, "module1", "test_test_case_1.py")
    )


@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch("kaizen.helpers.output.general.clean_python_code")
@mock.patch("kaizen.helpers.output.logger")
def test_create_test_files_no_tests(
    mock_logger, mock_clean_python_code, mock_create_folder
):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "high",
            "module_title": "Module 1",
            "tests": [],
        }
    ]
    folder_path = "test_folder"

    create_test_files(json_tests, folder_path)

    mock_create_folder.assert_called_once_with(os.path.join(folder_path, "module1"))
    mock_clean_python_code.assert_not_called()
    mock_logger.info.assert_not_called()

    with open(os.path.join(folder_path, "tests.json"), "r") as f:
        assert json.load(f) == json_tests

    assert not os.path.exists(
        os.path.join(folder_path, "module1", "test_test_case_1.py")
    )


@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch("kaizen.helpers.output.general.clean_python_code")
@mock.patch("kaizen.helpers.output.logger")
def test_create_test_files_special_characters(
    mock_logger, mock_clean_python_code, mock_create_folder
):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "high",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test@Case#1",
                    "test_description": "Description 1",
                    "code": "print('Hello World')",
                }
            ],
        }
    ]
    folder_path = "test_folder"
    mock_clean_python_code.return_value = "print('Hello World')"

    create_test_files(json_tests, folder_path)

    mock_create_folder.assert_called_once_with(os.path.join(folder_path, "module1"))
    mock_clean_python_code.assert_called_once_with("print('Hello World')")
    mock_logger.info.assert_not_called()

    with open(os.path.join(folder_path, "tests.json"), "r") as f:
        assert json.load(f) == json_tests

    with open(os.path.join(folder_path, "module1", "test_test_case_1.py"), "r") as f:
        content = f.read()
        assert "Importance: high" in content
        assert "Module Name: Module 1" in content
        assert "Description: Description 1" in content
        assert "print('Hello World')" in content
