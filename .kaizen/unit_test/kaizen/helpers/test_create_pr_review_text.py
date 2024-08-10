import pytest
from kaizen.helpers.output import create_pr_review_text

PR_COLLAPSIBLE_TEMPLATE = """
<details>
<summary>Review</summary>
<p>{comment}</p>
<p><strong>Reason:</strong> {reason}</p>
<p><strong>Solution:</strong> {solution}</p>
<p><strong>Confidence:</strong> {confidence}</p>
<p><strong>Lines:</strong> {start_line} - {end_line}</p>
<p><strong>File:</strong> {file_name}</p>
<p><strong>Severity:</strong> {severity}</p>
</details>
"""

@pytest.fixture
def mock_template(monkeypatch):
    monkeypatch.setattr("kaizen.helpers.output.PR_COLLAPSIBLE_TEMPLATE", PR_COLLAPSIBLE_TEMPLATE)

def test_single_topic_single_review(mock_template):
    topics = {
        "Security": [
            {
                "comment": "Use HTTPS",
                "reason": "Sensitive data",
                "solution": "Switch to HTTPS",
                "confidence": "high",
                "start_line": 10,
                "end_line": 20,
                "file_name": "app.py",
                "severity_level": 9,
            }
        ]
    }
    expected_output = (
        "## Code Review\n\n"
        "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
        "### Security\n\n"
        "<details>\n<summary>Review</summary>\n<p>Use HTTPS</p>\n"
        "<p><strong>Reason:</strong> Sensitive data</p>\n"
        "<p><strong>Solution:</strong> Switch to HTTPS</p>\n"
        "<p><strong>Confidence:</strong> high</p>\n"
        "<p><strong>Lines:</strong> 10 - 20</p>\n"
        "<p><strong>File:</strong> app.py</p>\n"
        "<p><strong>Severity:</strong> 9</p>\n</details>\n"
    )
    assert create_pr_review_text(topics) == expected_output

def test_multiple_topics_multiple_reviews(mock_template):
    topics = {
        "Security": [
            {
                "comment": "Use HTTPS",
                "reason": "Sensitive data",
                "solution": "Switch to HTTPS",
                "confidence": "high",
                "start_line": 10,
                "end_line": 20,
                "file_name": "app.py",
                "severity_level": 9,
            }
        ],
        "Performance": [
            {
                "comment": "Optimize query",
                "reason": "Slow response",
                "solution": "Add index",
                "confidence": "medium",
                "start_line": 30,
                "end_line": 40,
                "file_name": "db.py",
                "severity_level": 7,
            }
        ]
    }
    expected_output = (
        "## Code Review\n\n"
        "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
        "### Security\n\n"
        "<details>\n<summary>Review</summary>\n<p>Use HTTPS</p>\n"
        "<p><strong>Reason:</strong> Sensitive data</p>\n"
        "<p><strong>Solution:</strong> Switch to HTTPS</p>\n"
        "<p><strong>Confidence:</strong> high</p>\n"
        "<p><strong>Lines:</strong> 10 - 20</p>\n"
        "<p><strong>File:</strong> app.py</p>\n"
        "<p><strong>Severity:</strong> 9</p>\n</details>\n"
        "### Performance\n\n"
        "<details>\n<summary>Review</summary>\n<p>Optimize query</p>\n"
        "<p><strong>Reason:</strong> Slow response</p>\n"
        "<p><strong>Solution:</strong> Add index</p>\n"
        "<p><strong>Confidence:</strong> medium</p>\n"
        "<p><strong>Lines:</strong> 30 - 40</p>\n"
        "<p><strong>File:</strong> db.py</p>\n"
        "<p><strong>Severity:</strong> 7</p>\n</details>\n"
    )
    assert create_pr_review_text(topics) == expected_output

def test_empty_topics(mock_template):
    topics = {}
    expected_output = (
        "## Code Review\n\n"
        "✅ **All Clear:** This PR is ready to merge! 👍\n\n"
    )
    assert create_pr_review_text(topics) == expected_output

def test_topics_with_empty_reviews(mock_template):
    topics = {
        "Security": [],
        "Performance": []
    }
    expected_output = (
        "## Code Review\n\n"
        "✅ **All Clear:** This PR is ready to merge! 👍\n\n"
    )
    assert create_pr_review_text(topics) == expected_output

def test_missing_keys_in_review(mock_template):
    topics = {
        "Security": [
            {
                "comment": "Use HTTPS",
                "reason": "Sensitive data",
                "solution": "Switch to HTTPS",
                "confidence": "high",
                "start_line": 10,
                "end_line": 20,
                "file_name": "app.py",
                # Missing severity_level
            }
        ]
    }
    expected_output = (
        "## Code Review\n\n"
        "✅ **All Clear:** This PR is ready to merge! 👍\n\n"
        "### Security\n\n"
        "<details>\n<summary>Review</summary>\n<p>Use HTTPS</p>\n"
        "<p><strong>Reason:</strong> Sensitive data</p>\n"
        "<p><strong>Solution:</strong> Switch to HTTPS</p>\n"
        "<p><strong>Confidence:</strong> high</p>\n"
        "<p><strong>Lines:</strong> 10 - 20</p>\n"
        "<p><strong>File:</strong> app.py</p>\n"
        "<p><strong>Severity:</strong> NA</p>\n</details>\n"
    )
    assert create_pr_review_text(topics) == expected_output

def test_high_ranked_issues_boundary(mock_template):
    topics = {
        "Security": [
            {
                "comment": "Use HTTPS",
                "reason": "Sensitive data",
                "solution": "Switch to HTTPS",
                "confidence": "critical",
                "start_line": 10,
                "end_line": 20,
                "file_name": "app.py",
                "severity_level": 8,
            }
        ]
    }
    expected_output = (
        "## Code Review\n\n"
        "✅ **All Clear:** This PR is ready to merge! 👍\n\n"
        "### Security\n\n"
        "<details>\n<summary>Review</summary>\n<p>Use HTTPS</p>\n"
        "<p><strong>Reason:</strong> Sensitive data</p>\n"
        "<p><strong>Solution:</strong> Switch to HTTPS</p>\n"
        "<p><strong>Confidence:</strong> critical</p>\n"
        "<p><strong>Lines:</strong> 10 - 20</p>\n"
        "<p><strong>File:</strong> app.py</p>\n"
        "<p><strong>Severity:</strong> 8</p>\n</details>\n"
    )
    assert create_pr_review_text(topics) == expected_output