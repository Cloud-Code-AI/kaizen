import os
import json
import pytest
from unittest import mock
from unittest.mock import patch

# Assuming the save_review function is imported from the specified path
from .experiments.code_review.main import save_review

@pytest.fixture
def setup_folder(tmp_path):
    # Create a temporary directory for testing
    return tmp_path

def test_save_review_valid_data(setup_folder):
    pr_number = 123
    review_desc = "This is a review description."
    comments = [{"line": 10, "comment": "Looks good!"}]
    issues = [{"issue": "Variable not used", "line": 15}]
    folder = setup_folder
    combined_diff_data = "diff --git a/file.txt b/file.txt"

    save_review(pr_number, review_desc, comments, issues, str(folder), combined_diff_data)

    # Verify files were created with correct content
    review_file = os.path.join(folder, f"pr_{pr_number}", "review.md")
    comments_file = os.path.join(folder, f"pr_{pr_number}", "comments.json")
    issues_file = os.path.join(folder, f"pr_{pr_number}", "issues.json")
    combined_diff = os.path.join(folder, f"pr_{pr_number}", "combined_diff.txt")

    assert os.path.exists(review_file)
    assert os.path.exists(comments_file)
    assert os.path.exists(issues_file)
    assert os.path.exists(combined_diff)

    with open(review_file, "r") as f:
        assert f.read() == review_desc

    with open(comments_file, "r") as f:
        assert json.load(f) == comments

    with open(issues_file, "r") as f:
        assert json.load(f) == issues

    with open(combined_diff, "r") as f:
        assert f.read() == combined_diff_data

def test_save_review_empty_data(setup_folder):
    pr_number = 456
    review_desc = ""
    comments = []
    issues = []
    folder = setup_folder
    combined_diff_data = ""

    save_review(pr_number, review_desc, comments, issues, str(folder), combined_diff_data)

    # Verify files were created with correct content
    review_file = os.path.join(folder, f"pr_{pr_number}", "review.md")
    comments_file = os.path.join(folder, f"pr_{pr_number}", "comments.json")
    issues_file = os.path.join(folder, f"pr_{pr_number}", "issues.json")
    combined_diff = os.path.join(folder, f"pr_{pr_number}", "combined_diff.txt")

    assert os.path.exists(review_file)
    assert os.path.exists(comments_file)
    assert os.path.exists(issues_file)
    assert os.path.exists(combined_diff)

    with open(review_file, "r") as f:
        assert f.read() == review_desc

    with open(comments_file, "r") as f:
        assert json.load(f) == comments

    with open(issues_file, "r") as f:
        assert json.load(f) == issues

    with open(combined_diff, "r") as f:
        assert f.read() == combined_diff_data

def test_save_review_empty_folder_path():
    pr_number = 789
    review_desc = "Review description"
    comments = [{"line": 20, "comment": "Needs improvement"}]
    issues = [{"issue": "Syntax error", "line": 25}]
    folder = ""
    combined_diff_data = "diff --git a/file2.txt b/file2.txt"

    with pytest.raises(FileNotFoundError):
        save_review(pr_number, review_desc, comments, issues, folder, combined_diff_data)

@patch("os.makedirs")
def test_save_review_invalid_folder_path(mock_makedirs):
    mock_makedirs.side_effect = OSError("Invalid folder path")
    pr_number = 101
    review_desc = "Another review description"
    comments = [{"line": 30, "comment": "Check this"}]
    issues = [{"issue": "Deprecated function", "line": 35}]
    folder = "/invalid/folder/path"
    combined_diff_data = "diff --git a/file3.txt b/file3.txt"

    with pytest.raises(OSError, match="Invalid folder path"):
        save_review(pr_number, review_desc, comments, issues, folder, combined_diff_data)