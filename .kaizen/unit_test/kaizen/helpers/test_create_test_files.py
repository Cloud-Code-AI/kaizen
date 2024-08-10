import os
import json
import pytest
from unittest.mock import patch, mock_open, MagicMock

# Assuming the function is imported from kaizen/helpers/output.py
from kaizen.helpers.output import create_test_files

@pytest.fixture
def mock_clean_python_code():
    with patch("kaizen.helpers.output.general.clean_python_code") as mock_clean:
        yield mock_clean

@pytest.fixture
def mock_create_folder():
    with patch("kaizen.helpers.output.create_folder") as mock_folder:
        yield mock_folder

@pytest.fixture
def mock_logger():
    with patch("kaizen.helpers.output.logger") as mock_log:
        yield mock_log

@pytest.fixture
def mock_open_file():
    with patch("builtins.open", mock_open()) as mock_file:
        yield mock_file

def test_single_module_single_test(mock_clean_python_code, mock_create_folder, mock_open_file):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test 1",
                    "test_description": "Description 1",
                    "code": "print('Hello, World!')"
                }
            ]
        }
    ]
    folder_path = "test_folder"
    mock_clean_python_code.return_value = "cleaned_code"

    create_test_files(json_tests, folder_path)

    mock_create_folder.assert_called_once_with(os.path.join(folder_path, "module1"))
    mock_open_file.assert_any_call(os.path.join(folder_path, "tests.json"), "w")
    mock_open_file.assert_any_call(os.path.join(folder_path, "module1", "test_test_1.py"), "w")
    mock_clean_python_code.assert_called_once_with("print('Hello, World!')")

def test_multiple_modules_multiple_tests(mock_clean_python_code, mock_create_folder, mock_open_file):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test 1",
                    "test_description": "Description 1",
                    "code": "print('Hello, World!')"
                }
            ]
        },
        {
            "folder_name": "module2",
            "importance": "Medium",
            "module_title": "Module 2",
            "tests": [
                {
                    "test_name": "Test 2",
                    "test_description": "Description 2",
                    "code": "print('Goodbye, World!')"
                }
            ]
        }
    ]
    folder_path = "test_folder"
    mock_clean_python_code.side_effect = ["cleaned_code1", "cleaned_code2"]

    create_test_files(json_tests, folder_path)

    assert mock_create_folder.call_count == 2
    mock_open_file.assert_any_call(os.path.join(folder_path, "tests.json"), "w")
    mock_open_file.assert_any_call(os.path.join(folder_path, "module1", "test_test_1.py"), "w")
    mock_open_file.assert_any_call(os.path.join(folder_path, "module2", "test_test_2.py"), "w")
    assert mock_clean_python_code.call_count == 2

def test_empty_json_tests(mock_create_folder, mock_open_file):
    json_tests = []
    folder_path = "test_folder"

    create_test_files(json_tests, folder_path)

    mock_create_folder.assert_not_called()
    mock_open_file.assert_called_once_with(os.path.join(folder_path, "tests.json"), "w")

def test_module_with_no_tests(mock_create_folder, mock_open_file):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "module_title": "Module 1",
            "tests": []
        }
    ]
    folder_path = "test_folder"

    create_test_files(json_tests, folder_path)

    mock_create_folder.assert_called_once_with(os.path.join(folder_path, "module1"))
    mock_open_file.assert_called_once_with(os.path.join(folder_path, "tests.json"), "w")

def test_cleaning_code_fails(mock_clean_python_code, mock_create_folder, mock_open_file, mock_logger):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test 1",
                    "test_description": "Description 1",
                    "code": "print('Hello, World!')"
                }
            ]
        }
    ]
    folder_path = "test_folder"
    mock_clean_python_code.return_value = ""

    create_test_files(json_tests, folder_path)

    mock_logger.info.assert_called_once_with("Failed to clean code")

@pytest.mark.parametrize("test_name", [
    ("Test with special characters!@#"),
    ("Test with spaces"),
    ("Test with a very very very very very very very very very long name")
])
def test_various_test_names(mock_clean_python_code, mock_create_folder, mock_open_file, test_name):
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": test_name,
                    "test_description": "Description",
                    "code": "print('Hello, World!')"
                }
            ]
        }
    ]
    folder_path = "test_folder"
    mock_clean_python_code.return_value = "cleaned_code"

    create_test_files(json_tests, folder_path)

    expected_file_name = "test_" + "_".join(test_name.lower().split(" ")) + ".py"
    mock_open_file.assert_any_call(os.path.join(folder_path, "module1", expected_file_name), "w")