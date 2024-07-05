import os
import json
import pytest
from unittest import mock
from kaizen.helpers.output import create_test_files


@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch("kaizen.helpers.output.general.clean_python_code")
@mock.patch("kaizen.helpers.output.logger")
def test_create_test_files_normal_case(
    mock_logger, mock_clean_python_code, mock_create_folder, tmp_path
):
    # Arrange
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test 1",
                    "test_description": "Description 1",
                    "code": "print('Hello World')",
                }
            ],
        }
    ]
    folder_path = tmp_path
    mock_clean_python_code.return_value = "print('Hello World')"

    # Act
    create_test_files(json_tests, folder_path)

    # Assert
    assert os.path.exists(os.path.join(folder_path, "tests.json"))
    with open(os.path.join(folder_path, "tests.json"), "r") as f:
        assert json.load(f) == json_tests

    module_folder_path = os.path.join(folder_path, "module1")
    mock_create_folder.assert_called_once_with(module_folder_path)

    test_file_path = os.path.join(module_folder_path, "test_test_1.py")
    assert os.path.exists(test_file_path)
    with open(test_file_path, "r") as f:
        content = f.read()
        assert "Importance: High" in content
        assert "Module Name: Module 1" in content
        assert "Description: Description 1" in content
        assert "print('Hello World')" in content


@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch("kaizen.helpers.output.general.clean_python_code")
@mock.patch("kaizen.helpers.output.logger")
def test_create_test_files_empty_code(
    mock_logger, mock_clean_python_code, mock_create_folder, tmp_path
):
    # Arrange
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test 1",
                    "test_description": "Description 1",
                    "code": "print('Hello World')",
                }
            ],
        }
    ]
    folder_path = tmp_path
    mock_clean_python_code.return_value = ""

    # Act
    create_test_files(json_tests, folder_path)

    # Assert
    mock_logger.info.assert_called_once_with("Failed to clean code")


@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch("kaizen.helpers.output.general.clean_python_code")
@mock.patch("kaizen.helpers.output.logger")
def test_create_test_files_no_tests(
    mock_logger, mock_clean_python_code, mock_create_folder, tmp_path
):
    # Arrange
    json_tests = []
    folder_path = tmp_path

    # Act
    create_test_files(json_tests, folder_path)

    # Assert
    assert os.path.exists(os.path.join(folder_path, "tests.json"))
    with open(os.path.join(folder_path, "tests.json"), "r") as f:
        assert json.load(f) == json_tests
    mock_create_folder.assert_not_called()
    mock_clean_python_code.assert_not_called()
    mock_logger.info.assert_not_called()


@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch("kaizen.helpers.output.general.clean_python_code")
@mock.patch("kaizen.helpers.output.logger")
def test_create_test_files_special_characters_in_test_name(
    mock_logger, mock_clean_python_code, mock_create_folder, tmp_path
):
    # Arrange
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "module_title": "Module 1",
            "tests": [
                {
                    "test_name": "Test@1!",
                    "test_description": "Description 1",
                    "code": "print('Hello World')",
                }
            ],
        }
    ]
    folder_path = tmp_path
    mock_clean_python_code.return_value = "print('Hello World')"

    # Act
    create_test_files(json_tests, folder_path)

    # Assert
    module_folder_path = os.path.join(folder_path, "module1")
    mock_create_folder.assert_called_once_with(module_folder_path)

    test_file_path = os.path.join(module_folder_path, "test_test_1.py")
    assert os.path.exists(test_file_path)
    with open(test_file_path, "r") as f:
        content = f.read()
        assert "Importance: High" in content
        assert "Module Name: Module 1" in content
        assert "Description: Description 1" in content
        assert "print('Hello World')" in content


@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch("kaizen.helpers.output.general.clean_python_code")
@mock.patch("kaizen.helpers.output.logger")
def test_create_test_files_invalid_json(
    mock_logger, mock_clean_python_code, mock_create_folder, tmp_path
):
    # Arrange
    json_tests = "invalid_json"
    folder_path = tmp_path

    # Act & Assert
    with pytest.raises(TypeError):
        create_test_files(json_tests, folder_path)


@mock.patch("kaizen.helpers.output.create_folder")
@mock.patch("kaizen.helpers.output.general.clean_python_code")
@mock.patch("kaizen.helpers.output.logger")
def test_create_test_files_missing_keys(
    mock_logger, mock_clean_python_code, mock_create_folder, tmp_path
):
    # Arrange
    json_tests = [
        {
            "folder_name": "module1",
            "importance": "High",
            "tests": [
                {
                    "test_name": "Test 1",
                    "test_description": "Description 1",
                    "code": "print('Hello World')",
                }
            ],
        }
    ]
    folder_path = tmp_path
    mock_clean_python_code.return_value = "print('Hello World')"

    # Act
    create_test_files(json_tests, folder_path)

    # Assert
    module_folder_path = os.path.join(folder_path, "module1")
    mock_create_folder.assert_called_once_with(module_folder_path)

    test_file_path = os.path.join(module_folder_path, "test_test_1.py")
    assert os.path.exists(test_file_path)
    with open(test_file_path, "r") as f:
        content = f.read()
        assert "Importance: High" in content
        assert "Description: Description 1" in content
        assert "print('Hello World')" in content
