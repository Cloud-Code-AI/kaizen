import pytest
from unittest import mock
from kaizen.helpers.output import get_parent_folder


def test_get_parent_folder_normal_case():
    with mock.patch("os.getcwd", return_value="/home/user/project"):
        assert get_parent_folder() == "/home/user/project"


def test_get_parent_folder_edge_case_root_directory():
    with mock.patch("os.getcwd", return_value="/"):
        assert get_parent_folder() == "/"


def test_get_parent_folder_edge_case_empty_string():
    with mock.patch("os.getcwd", return_value=""):
        assert get_parent_folder() == ""


def test_get_parent_folder_error_handling():
    with mock.patch(
        "os.getcwd", side_effect=OSError("Failed to get current working directory")
    ):
        with pytest.raises(OSError, match="Failed to get current working directory"):
            get_parent_folder()


def test_get_parent_folder_boundary_condition_long_path():
    long_path = "/" + "a" * 255
    with mock.patch("os.getcwd", return_value=long_path):
        assert get_parent_folder() == long_path
