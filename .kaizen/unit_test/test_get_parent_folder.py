import os
import pytest
from unittest import mock
from kaizen.helpers.output import get_parent_folder


def test_get_parent_folder_normal_case():
    with mock.patch("os.getcwd", return_value="/home/user/folder"):
        assert get_parent_folder() == "/home/user/folder"


def test_get_parent_folder_edge_case_root_directory():
    with mock.patch("os.getcwd", return_value="/"):
        assert get_parent_folder() == "/"


def test_get_parent_folder_edge_case_empty_string():
    with mock.patch("os.getcwd", return_value=""):
        assert get_parent_folder() == ""


def test_get_parent_folder_error_handling():
    with mock.patch(
        "os.getcwd", side_effect=OSError("Failed to get current directory")
    ):
        with pytest.raises(OSError, match="Failed to get current directory"):
            get_parent_folder()


def test_get_parent_folder_boundary_condition_long_path():
    long_path = "/" + "a" * 255
    with mock.patch("os.getcwd", return_value=long_path):
        assert get_parent_folder() == long_path


def test_get_parent_folder_with_special_characters():
    special_path = "/home/user/folder with spaces and !@#$%^&*()"
    with mock.patch("os.getcwd", return_value=special_path):
        assert get_parent_folder() == special_path


def test_get_parent_folder_with_unicode_characters():
    unicode_path = "/home/user/文件夹"
    with mock.patch("os.getcwd", return_value=unicode_path):
        assert get_parent_folder() == unicode_path
