import pytest
from unittest import mock
from kaizen.helpers.output import get_parent_folder


def test_get_parent_folder_normal_case():
    with mock.patch("os.getcwd", return_value="/home/user/project"):
        result = get_parent_folder()
        assert result == "/home/user/project"


def test_get_parent_folder_edge_case_root_directory():
    with mock.patch("os.getcwd", return_value="/"):
        result = get_parent_folder()
        assert result == "/"


def test_get_parent_folder_edge_case_empty_string():
    with mock.patch("os.getcwd", return_value=""):
        result = get_parent_folder()
        assert result == ""


def test_get_parent_folder_error_handling():
    with mock.patch(
        "os.getcwd", side_effect=OSError("Unable to get current working directory")
    ):
        with pytest.raises(OSError, match="Unable to get current working directory"):
            get_parent_folder()


def test_get_parent_folder_boundary_condition_long_path():
    long_path = "/" + "a" * 255
    with mock.patch("os.getcwd", return_value=long_path):
        result = get_parent_folder()
        assert result == long_path


def test_get_parent_folder_with_trailing_slash():
    with mock.patch("os.getcwd", return_value="/home/user/project/"):
        result = get_parent_folder()
        assert result == "/home/user/project/"


def test_get_parent_folder_with_special_characters():
    special_path = "/home/user/project_!@#$/folder"
    with mock.patch("os.getcwd", return_value=special_path):
        result = get_parent_folder()
        assert result == special_path
