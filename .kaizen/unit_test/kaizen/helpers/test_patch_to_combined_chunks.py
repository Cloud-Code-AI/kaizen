import pytest
from kaizen.helpers.parser import patch_to_combined_chunks

# Mock the format_change function used in the source code
def format_change(file_name, line_num, change_type, content, ignore_deletions):
    return f"{change_type}: {content}"

@pytest.fixture
def mock_format_change(monkeypatch):
    monkeypatch.setattr("builtins.format_change", format_change)

def test_empty_patch_text(mock_format_change):
    result = patch_to_combined_chunks("")
    assert result == ""

def test_single_file_addition(mock_format_change):
    patch_text = """diff --git a/file.txt b/file.txt
--- a/file.txt
+++ b/file.txt
@@ -0,0 +1 @@
+new line
"""
    expected_output = "\n[FILE_START] file.txt\n\nUPDATED: new line"
    result = patch_to_combined_chunks(patch_text)
    assert result == expected_output

def test_single_file_deletion(mock_format_change):
    patch_text = """diff --git a/file.txt b/file.txt
--- a/file.txt
+++ b/file.txt
@@ -1 +0,0 @@
-old line
"""
    expected_output = "\n[FILE_START] file.txt\n\nREMOVED: old line"
    result = patch_to_combined_chunks(patch_text)
    assert result == expected_output

def test_ignore_deletions(mock_format_change):
    patch_text = """diff --git a/file.txt b/file.txt
--- a/file.txt
+++ b/file.txt
@@ -1 +0,0 @@
-old line
"""
    expected_output = "\n[FILE_START] file.txt\n"
    result = patch_to_combined_chunks(patch_text, ignore_deletions=True)
    assert result == expected_output

def test_context_lines(mock_format_change):
    patch_text = """diff --git a/file.txt b/file.txt
--- a/file.txt
+++ b/file.txt
@@ -1,3 +1,3 @@
 line 1
-line 2
+line 2 updated
 line 3
"""
    expected_output = (
        "\n[FILE_START] file.txt\n\n"
        "CONTEXT: line 1\n"
        "REMOVED: line 2\n"
        "UPDATED: line 2 updated\n"
        "CONTEXT: line 3"
    )
    result = patch_to_combined_chunks(patch_text)
    assert result == expected_output