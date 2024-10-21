# test_group_by_files.py

import pytest
from examples.code_fix.main import group_by_files

def test_group_by_single_file():
    issues = [
        {"file_path": "file1.py", "issue": "error1"},
        {"file_path": "file1.py", "issue": "error2"}
    ]
    expected = {
        "file1.py": [
            {"file_path": "file1.py", "issue": "error1"},
            {"file_path": "file1.py", "issue": "error2"}
        ]
    }
    assert group_by_files(issues) == expected

def test_group_by_multiple_files():
    issues = [
        {"file_path": "file1.py", "issue": "error1"},
        {"file_path": "file2.py", "issue": "error2"},
        {"file_path": "file1.py", "issue": "error3"}
    ]
    expected = {
        "file1.py": [
            {"file_path": "file1.py", "issue": "error1"},
            {"file_path": "file1.py", "issue": "error3"}
        ],
        "file2.py": [
            {"file_path": "file2.py", "issue": "error2"}
        ]
    }
    assert group_by_files(issues) == expected

def test_empty_issues_list():
    issues = []
    expected = {}
    assert group_by_files(issues) == expected

def test_issue_without_file_path_key():
    issues = [
        {"issue": "error1"}
    ]
    with pytest.raises(KeyError):
        group_by_files(issues)