import pytest
from unittest import mock
from kaizen.helpers.output import get_parent_folder


def test_get_parent_folder_returns_current_directory():
    expected_directory = "/home/user"
    with mock.patch("os.getcwd", return_value=expected_directory):
        assert get_parent_folder() == expected_directory


def test_get_parent_folder_with_different_directory():
    expected_directory = "/var/log"
    with mock.patch("os.getcwd", return_value=expected_directory):
        assert get_parent_folder() == expected_directory


def test_get_parent_folder_with_empty_directory():
    expected_directory = ""
    with mock.patch("os.getcwd", return_value=expected_directory):
        assert get_parent_folder() == expected_directory


def test_get_parent_folder_with_root_directory():
    expected_directory = "/"
    with mock.patch("os.getcwd", return_value=expected_directory):
        assert get_parent_folder() == expected_directory


def test_get_parent_folder_with_special_characters_directory():
    expected_directory = "/home/user/!@#$%^&*()"
    with mock.patch("os.getcwd", return_value=expected_directory):
        assert get_parent_folder() == expected_directory


def test_get_parent_folder_with_long_directory_path():
    expected_directory = "/a" * 255
    with mock.patch("os.getcwd", return_value=expected_directory):
        assert get_parent_folder() == expected_directory


def test_get_parent_folder_raises_exception():
    with mock.patch(
        "os.getcwd", side_effect=Exception("Unable to get current directory")
    ):
        with pytest.raises(Exception, match="Unable to get current directory"):
            get_parent_folder()
