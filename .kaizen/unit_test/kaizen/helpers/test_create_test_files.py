import os
import json
import pytest
from unittest import mock
from kaizen.helpers.output import create_test_files

# Mocking dependencies
@pytest.fixture
def mock_dependencies():
    with mock.patch('kaizen.helpers.output.create_folder') as mock_create_folder, \
         mock.patch('kaizen.helpers.output.general.clean_python_code') as mock_clean_python_code, \
         mock.patch('kaizen.helpers.output.logger') as mock_logger:
        yield mock_create_folder, mock_clean_python_code, mock_logger

# Utility function to read file content
def read_file_content(file_path):
    with open(file_path, 'r') as f:
        return f.read()

# Utility function to sanitize file names
def sanitize_filename(filename):
    return "".join(c if c.isalnum() or c in (' ', '.', '_') else '_' for c in filename)

# Test single module with a single test
def test_single_module_single_test(tmp_path, mock_dependencies):
    mock_create_folder, mock_clean_python_code, mock_logger = mock_dependencies
    mock_clean_python_code.return_value = "def test_example():\n    assert True"

    json_tests = [{
        "folder_name": "module1",
        "module_title": "Module 1",
        "importance": "High",
        "tests": [{
            "test_name": "Test Example",
            "test_description": "This is a test example.",
            "code": "def test_example():\n    assert True"
        }]
    }]

    create_test_files(json_tests, tmp_path)

    # Assertions
    assert os.path.exists(os.path.join(tmp_path, "tests.json"))
    assert os.path.exists(os.path.join(tmp_path, "module1", "test_test_example.py"))
    assert "Importance: High" in read_file_content(os.path.join(tmp_path, "module1", "test_test_example.py"))

# Test multiple modules with multiple tests
def test_multiple_modules_multiple_tests(tmp_path, mock_dependencies):
    mock_create_folder, mock_clean_python_code, mock_logger = mock_dependencies
    mock_clean_python_code.return_value = "def test_example():\n    assert True"

    json_tests = [
        {
            "folder_name": "module1",
            "module_title": "Module 1",
            "importance": "High",
            "tests": [
                {
                    "test_name": "Test Example 1",
                    "test_description": "This is test example 1.",
                    "code": "def test_example_1():\n    assert True"
                },
                {
                    "test_name": "Test Example 2",
                    "test_description": "This is test example 2.",
                    "code": "def test_example_2():\n    assert True"
                }
            ]
        },
        {
            "folder_name": "module2",
            "module_title": "Module 2",
            "importance": "Medium",
            "tests": [
                {
                    "test_name": "Test Example 3",
                    "test_description": "This is test example 3.",
                    "code": "def test_example_3():\n    assert True"
                }
            ]
        }
    ]

    create_test_files(json_tests, tmp_path)

    # Assertions
    assert os.path.exists(os.path.join(tmp_path, "tests.json"))
    assert os.path.exists(os.path.join(tmp_path, "module1", "test_test_example_1.py"))
    assert os.path.exists(os.path.join(tmp_path, "module1", "test_test_example_2.py"))
    assert os.path.exists(os.path.join(tmp_path, "module2", "test_test_example_3.py"))

# Test empty json_tests list
def test_empty_json_tests(tmp_path, mock_dependencies):
    mock_create_folder, mock_clean_python_code, mock_logger = mock_dependencies

    json_tests = []

    create_test_files(json_tests, tmp_path)

    # Assertions
    assert os.path.exists(os.path.join(tmp_path, "tests.json"))
    assert os.path.getsize(os.path.join(tmp_path, "tests.json")) == 0

# Test names with special characters
def test_special_characters_in_test_names(tmp_path, mock_dependencies):
    mock_create_folder, mock_clean_python_code, mock_logger = mock_dependencies
    mock_clean_python_code.return_value = "def test_example():\n    assert True"

    json_tests = [{
        "folder_name": "module1",
        "module_title": "Module 1",
        "importance": "High",
        "tests": [{
            "test_name": "Test Example!@#",
            "test_description": "This is a test example with special characters.",
            "code": "def test_example():\n    assert True"
        }]
    }]

    create_test_files(json_tests, tmp_path)

    # Assertions
    sanitized_name = sanitize_filename("test_test_example!@#.py")
    assert os.path.exists(os.path.join(tmp_path, "module1", sanitized_name))

# Test very long test names
def test_very_long_test_names(tmp_path, mock_dependencies):
    mock_create_folder, mock_clean_python_code, mock_logger = mock_dependencies
    mock_clean_python_code.return_value = "def test_example():\n    assert True"

    long_test_name = "Test " + "Example " * 50
    json_tests = [{
        "folder_name": "module1",
        "module_title": "Module 1",
        "importance": "High",
        "tests": [{
            "test_name": long_test_name,
            "test_description": "This is a very long test name.",
            "code": "def test_example():\n    assert True"
        }]
    }]

    create_test_files(json_tests, tmp_path)

    # Assertions
    file_name = "test_" + "_".join(long_test_name.lower().split(" ")) + ".py"
    assert os.path.exists(os.path.join(tmp_path, "module1", file_name))
    assert len(file_name) <= 255  # Assuming a common file system limit
    assert "def test_example():\n    assert True" in read_file_content(os.path.join(tmp_path, "module1", file_name))

# Test clean code function returns empty string
def test_clean_code_returns_empty_string(tmp_path, mock_dependencies):
    mock_create_folder, mock_clean_python_code, mock_logger = mock_dependencies
    mock_clean_python_code.return_value = ""

    json_tests = [{
        "folder_name": "module1",
        "module_title": "Module 1",
        "importance": "High",
        "tests": [{
            "test_name": "Test Example",
            "test_description": "This is a test example.",
            "code": "def test_example():\n    assert True"
        }]
    }]

    create_test_files(json_tests, tmp_path)

    # Assertions
    mock_logger.info.assert_called_with("Failed to clean code")
    assert not os.path.exists(os.path.join(tmp_path, "module1", "test_test_example.py"))
    assert not os.path.exists(os.path.join(tmp_path, "tests.json"))

# Test file writing permission issues
def test_file_writing_permission_issues(tmp_path, mock_dependencies):
    mock_create_folder, mock_clean_python_code, mock_logger = mock_dependencies
    mock_clean_python_code.return_value = "def test_example():\n    assert True"

    json_tests = [{
        "folder_name": "module1",
        "module_title": "Module 1",
        "importance": "High",
        "tests": [{
            "test_name": "Test Example",
            "test_description": "This is a test example.",
            "code": "def test_example():\n    assert True"
        }]
    }]

    # Simulate permission error
    with mock.patch("builtins.open", mock.mock_open()) as mock_file:
        mock_file.side_effect = PermissionError

        with pytest.raises(PermissionError):
            create_test_files(json_tests, tmp_path)

    # Assertions
    assert not os.path.exists(os.path.join(tmp_path, "tests.json"))

# Test maximum number of modules
def test_maximum_number_of_modules(tmp_path, mock_dependencies):
    mock_create_folder, mock_clean_python_code, mock_logger = mock_dependencies
    mock_clean_python_code.return_value = "def test_example():\n    assert True"

    json_tests = [
        {
            "folder_name": f"module{i}",
            "module_title": f"Module {i}",
            "importance": "High",
            "tests": [{
                "test_name": f"Test Example {i}",
                "test_description": f"This is test example {i}.",
                "code": "def test_example():\n    assert True"
            }]
        } for i in range(100)
    ]

    create_test_files(json_tests, tmp_path)

    # Assertions
    for i in range(100):
        assert os.path.exists(os.path.join(tmp_path, f"module{i}", f"test_test_example_{i}.py"))

# Test maximum number of tests per module
def test_maximum_number_of_tests_per_module(tmp_path, mock_dependencies):
    mock_create_folder, mock_clean_python_code, mock_logger = mock_dependencies
    mock_clean_python_code.return_value = "def test_example():\n    assert True"

    json_tests = [{
        "folder_name": "module1",
        "module_title": "Module 1",
        "importance": "High",
        "tests": [
            {
                "test_name": f"Test Example {i}",
                "test_description": f"This is test example {i}.",
                "code": "def test_example():\n    assert True"
            } for i in range(100)
        ]
    }]

    create_test_files(json_tests, tmp_path)

    # Assertions
    for i in range(100):
        assert os.path.exists(os.path.join(tmp_path, "module1", f"test_test_example_{i}.py"))