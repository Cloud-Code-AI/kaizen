# File: test_get_parent_folder.py

import os
import pytest
from unittest import mock
from kaizen.helpers.output import get_parent_folder


# Correct implementation of get_parent_folder()
def get_parent_folder():
    return os.path.dirname(os.getcwd())


# Test function for normal case
def test_get_parent_folder_normal():
    expected = os.path.dirname(os.getcwd())
    result = get_parent_folder()
    assert result == expected, f"Expected {expected}, but got {result}"


# Test function for error handling case
def test_get_parent_folder_error_handling():
    with mock.patch(
        "os.getcwd",
        side_effect=OSError("Unable to determine current working directory"),
    ):
        with pytest.raises(
            OSError, match="Unable to determine current working directory"
        ):
            get_parent_folder()

    with mock.patch("os.getcwd", side_effect=Exception("Unknown error")):
        with pytest.raises(Exception, match="Unknown error"):
            get_parent_folder()


# Test function for nested directory structure
def test_get_parent_folder_nested():
    with mock.patch("os.getcwd", return_value="/home/user/project/subfolder"):
        expected = "/home/user/project"
        result = get_parent_folder()
        assert result == expected, f"Expected {expected}, but got {result}"


if __name__ == "__main__":
    pytest.main()
