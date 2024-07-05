import pytest
from kaizen.helpers.output import create_pr_review_text

PR_COLLAPSIBLE_TEMPLATE = (
    "<details>\n"
    "<summary>Comment</summary>\n"
    "<p>{comment}</p>\n"
    "<p><strong>Reasoning:</strong>{reasoning}</p>\n"
    "<p><strong>Solution:</strong>{solution}</p>\n"
    "<p><strong>Confidence:</strong>{confidence}</p>\n"
    "<p><strong>Position:</strong>{position}</p>\n"
    "<p><strong>End Line:</strong>{end_line}</p>\n"
    "<p><strong>File Name:</strong>{file_name}</p>\n"
    "<p><strong>Request for Change:</strong>{request_for_change}</p>\n"
    "</details>\n"
)


@pytest.fixture(autouse=True)
def mock_template(monkeypatch):
    monkeypatch.setattr(
        "kaizen.helpers.output.PR_COLLAPSIBLE_TEMPLATE", PR_COLLAPSIBLE_TEMPLATE
    )


def test_create_pr_review_text_no_issues():
    topics = {
        "Topic1": [
            {
                "comment": "Comment1",
                "reasoning": "Reasoning1",
                "solution": "Solution1",
                "confidence": "low",
                "position": "Position1",
                "end_line": "EndLine1",
                "file_name": "FileName1",
                "request_for_change": "No",
            }
        ]
    }
    expected_output = (
        "## Code Review\n\n"
        "✅ **All Clear:** This PR is ready to merge! 👍\n\n"
        "### Topic1\n\n"
        "<details>\n"
        "<summary>Comment</summary>\n"
        "<p>Comment1</p>\n"
        "<p><strong>Reasoning:</strong> Reasoning1</p>\n"
        "<p><strong>Solution:</strong> Solution1</p>\n"
        "<p><strong>Confidence:</strong> low</p>\n"
        "<p><strong>Position:</strong> Position1</p>\n"
        "<p><strong>End Line:</strong> EndLine1</p>\n"
        "<p><strong>File Name:</strong> FileName1</p>\n"
        "<p><strong>Request for Change:</strong> No</p>\n"
        "</details>\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_with_critical_issues():
    topics = {
        "Topic1": [
            {
                "comment": "Comment1",
                "reasoning": "Reasoning1",
                "solution": "Solution1",
                "confidence": "critical",
                "position": "Position1",
                "end_line": "EndLine1",
                "file_name": "FileName1",
                "request_for_change": "Yes",
            }
        ]
    }
    expected_output = (
        "## Code Review\n\n"
        "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
        "### Topic1\n\n"
        "<details>\n"
        "<summary>Comment</summary>\n"
        "<p>Comment1</p>\n"
        "<p><strong>Reasoning:</strong> Reasoning1</p>\n"
        "<p><strong>Solution:</strong> Solution1</p>\n"
        "<p><strong>Confidence:</strong> critical</p>\n"
        "<p><strong>Position:</strong> Position1</p>\n"
        "<p><strong>End Line:</strong> EndLine1</p>\n"
        "<p><strong>File Name:</strong> FileName1</p>\n"
        "<p><strong>Request for Change:</strong> Yes</p>\n"
        "</details>\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_empty_topics():
    topics = {}
    expected_output = (
        "## Code Review\n\n" "✅ **All Clear:** This PR is ready to merge! 👍\n\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_multiple_topics():
    topics = {
        "Topic1": [
            {
                "comment": "Comment1",
                "reasoning": "Reasoning1",
                "solution": "Solution1",
                "confidence": "low",
                "position": "Position1",
                "end_line": "EndLine1",
                "file_name": "FileName1",
                "request_for_change": "No",
            }
        ],
        "Topic2": [
            {
                "comment": "Comment2",
                "reasoning": "Reasoning2",
                "solution": "Solution2",
                "confidence": "critical",
                "position": "Position2",
                "end_line": "EndLine2",
                "file_name": "FileName2",
                "request_for_change": "Yes",
            }
        ],
    }
    expected_output = (
        "## Code Review\n\n"
        "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
        "### Topic1\n\n"
        "<details>\n"
        "<summary>Comment</summary>\n"
        "<p>Comment1</p>\n"
        "<p><strong>Reasoning:</strong> Reasoning1</p>\n"
        "<p><strong>Solution:</strong> Solution1</p>\n"
        "<p><strong>Confidence:</strong> low</p>\n"
        "<p><strong>Position:</strong> Position1</p>\n"
        "<p><strong>End Line:</strong> EndLine1</p>\n"
        "<p><strong>File Name:</strong> FileName1</p>\n"
        "<p><strong>Request for Change:</strong> No</p>\n"
        "</details>\n"
        "### Topic2\n\n"
        "<details>\n"
        "<summary>Comment</summary>\n"
        "<p>Comment2</p>\n"
        "<p><strong>Reasoning:</strong> Reasoning2</p>\n"
        "<p><strong>Solution:</strong> Solution2</p>\n"
        "<p><strong>Confidence:</strong> critical</p>\n"
        "<p><strong>Position:</strong> Position2</p>\n"
        "<p><strong>End Line:</strong> EndLine2</p>\n"
        "<p><strong>File Name:</strong> FileName2</p>\n"
        "<p><strong>Request for Change:</strong> Yes</p>\n"
        "</details>\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_missing_fields():
    topics = {
        "Topic1": [
            {
                "comment": "Comment1",
                "reasoning": "Reasoning1",
                # Missing other fields
            }
        ]
    }
    expected_output = (
        "## Code Review\n\n"
        "✅ **All Clear:** This PR is ready to merge! 👍\n\n"
        "### Topic1\n\n"
        "<details>\n"
        "<summary>Comment</summary>\n"
        "<p>Comment1</p>\n"
        "<p><strong>Reasoning:</strong> Reasoning1</p>\n"
        "<p><strong>Solution:</strong> NA</p>\n"
        "<p><strong>Confidence:</strong> NA</p>\n"
        "<p><strong>Position:</strong> NA</p>\n"
        "<p><strong>End Line:</strong> NA</p>\n"
        "<p><strong>File Name:</strong> NA</p>\n"
        "<p><strong>Request for Change:</strong> NA</p>\n"
        "</details>\n"
    )
    assert create_pr_review_text(topics) == expected_output
