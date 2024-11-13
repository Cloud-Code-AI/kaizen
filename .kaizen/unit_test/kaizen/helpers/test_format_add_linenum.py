import pytest
from kaizen.helpers.parser import format_add_linenum

@pytest.mark.parametrize("new_num, content, expected", [
    (123, "Sample content", "123   Sample content"),
    (None, "Sample content", "     Sample content"),
    (12345, "Sample content", "12345 Sample content"),
    (123, "", "123   "),
    (None, "", "     "),
])
def test_format_add_linenum_basic_cases(new_num, content, expected):
    assert format_add_linenum(new_num, content) == expected

def test_format_add_linenum_multiline_content():
    multiline_content = "Line 1\nLine 2\nLine 3"
    expected = "123   Line 1\n123   Line 2\n123   Line 3"
    result = "\n".join(format_add_linenum(123, line) for line in multiline_content.split("\n"))
    assert result == expected

def test_format_add_linenum_ignore_deletions():
    # Since ignore_deletions is not used, this test checks that it doesn't affect the output
    assert format_add_linenum(123, "Content", ignore_deletions=True) == "123   Content"
    assert format_add_linenum(123, "Content", ignore_deletions=False) == "123   Content"