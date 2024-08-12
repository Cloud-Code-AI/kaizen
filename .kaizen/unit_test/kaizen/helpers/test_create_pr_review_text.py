import pytest
from kaizen.helpers.output import create_pr_review_text

PR_COLLAPSIBLE_TEMPLATE = """
<details>
<summary>Review Comment</summary>
<p>{comment}</p>
<p><strong>Reason:</strong> {reason}</p>
<p><strong>Solution:</strong> {solution}</p>
<p><strong>Confidence:</strong> {confidence}</p>
<p><strong>Start Line:</strong> {start_line}</p>
<p><strong>End Line:</strong> {end_line}</p>
<p><strong>File Name:</strong> {file_name}</p>
<p><strong>Severity:</strong> {severity}</p>
</details>
"""


@pytest.fixture
def setup_single_topic_single_review():
    return {
        "topic1": [
            {
                "comment": "This is a test comment.",
                "reason": "This is a test reason.",
                "solution": "This is a test solution.",
                "confidence": "critical",
                "start_line": 10,
                "end_line": 20,
                "file_name": "test_file.py",
                "severity_level": 9,
            }
        ]
    }


@pytest.fixture
def setup_multiple_topics_multiple_reviews():
    return {
        "topic1": [
            {
                "comment": "First comment.",
                "reason": "First reason.",
                "solution": "First solution.",
                "confidence": "critical",
                "start_line": 10,
                "end_line": 20,
                "file_name": "file1.py",
                "severity_level": 9,
            },
            {
                "comment": "Second comment.",
                "reason": "Second reason.",
                "solution": "Second solution.",
                "confidence": "high",
                "start_line": 30,
                "end_line": 40,
                "file_name": "file2.py",
                "severity_level": 7,
            },
        ],
        "topic2": [
            {
                "comment": "Third comment.",
                "reason": "Third reason.",
                "solution": "Third solution.",
                "confidence": "medium",
                "start_line": 50,
                "end_line": 60,
                "file_name": "file3.py",
                "severity_level": 5,
            }
        ],
    }


def test_empty_topics():
    topics = {}
    expected_output = (
        "## Code Review\n\n✅ **All Clear:** This PR is ready to merge! 👍\n\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_single_topic_single_review(setup_single_topic_single_review):
    topics = setup_single_topic_single_review
    expected_output = (
        "## Code Review\n\n"
        "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
        "### topic1\n\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="This is a test comment.",
            reason="This is a test reason.",
            solution="This is a test solution.",
            confidence="critical",
            start_line=10,
            end_line=20,
            file_name="test_file.py",
            severity=9,
        )
        + "\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_multiple_topics_multiple_reviews(setup_multiple_topics_multiple_reviews):
    topics = setup_multiple_topics_multiple_reviews
    expected_output = (
        "## Code Review\n\n"
        "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
        "### topic1\n\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="First comment.",
            reason="First reason.",
            solution="First solution.",
            confidence="critical",
            start_line=10,
            end_line=20,
            file_name="file1.py",
            severity=9,
        )
        + "\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="Second comment.",
            reason="Second reason.",
            solution="Second solution.",
            confidence="high",
            start_line=30,
            end_line=40,
            file_name="file2.py",
            severity=7,
        )
        + "\n"
        + "### topic2\n\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="Third comment.",
            reason="Third reason.",
            solution="Third solution.",
            confidence="medium",
            start_line=50,
            end_line=60,
            file_name="file3.py",
            severity=5,
        )
        + "\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_reviews_with_missing_fields():
    topics = {
        "topic1": [
            {
                "comment": "This is a test comment.",
                "reason": "This is a test reason.",
                # Missing solution
                "confidence": "critical",
                "start_line": 10,
                "end_line": 20,
                "file_name": "test_file.py",
                "severity_level": 9,
            },
            {
                "comment": "Another test comment.",
                # Missing reason
                "solution": "Another test solution.",
                "confidence": "high",
                "start_line": 30,
                "end_line": 40,
                "file_name": "another_test_file.py",
                "severity_level": 7,
            },
            {
                "comment": "Yet another test comment.",
                "reason": "Yet another test reason.",
                "solution": "Yet another test solution.",
                # Missing confidence
                "start_line": 50,
                "end_line": 60,
                "file_name": "yet_another_test_file.py",
                "severity_level": 5,
            },
            {
                "comment": "Final test comment.",
                "reason": "Final test reason.",
                "solution": "Final test solution.",
                "confidence": "low",
                "start_line": 70,
                "end_line": 80,
                "file_name": "final_test_file.py",
                # Missing severity_level
            },
        ]
    }
    expected_output = (
        "## Code Review\n\n"
        "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
        "### topic1\n\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="This is a test comment.",
            reason="This is a test reason.",
            solution="NA",
            confidence="critical",
            start_line=10,
            end_line=20,
            file_name="test_file.py",
            severity=9,
        )
        + "\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="Another test comment.",
            reason="NA",
            solution="Another test solution.",
            confidence="high",
            start_line=30,
            end_line=40,
            file_name="another_test_file.py",
            severity=7,
        )
        + "\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="Yet another test comment.",
            reason="Yet another test reason.",
            solution="Yet another test solution.",
            confidence="NA",
            start_line=50,
            end_line=60,
            file_name="yet_another_test_file.py",
            severity=5,
        )
        + "\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="Final test comment.",
            reason="Final test reason.",
            solution="Final test solution.",
            confidence="low",
            start_line=70,
            end_line=80,
            file_name="final_test_file.py",
            severity="NA",
        )
        + "\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_reviews_with_missing_comment():
    topics = {
        "topic1": [
            {
                # Missing comment
                "reason": "This is a test reason.",
                "solution": "This is a test solution.",
                "confidence": "critical",
                "start_line": 10,
                "end_line": 20,
                "file_name": "test_file.py",
                "severity_level": 9,
            }
        ]
    }
    expected_output = (
        "## Code Review\n\n"
        "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
        "### topic1\n\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="NA",
            reason="This is a test reason.",
            solution="This is a test solution.",
            confidence="critical",
            start_line=10,
            end_line=20,
            file_name="test_file.py",
            severity=9,
        )
        + "\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_empty_list_in_topics():
    topics = {"topic1": []}
    expected_output = (
        "## Code Review\n\n✅ **All Clear:** This PR is ready to merge! 👍\n\n"
    )
    assert create_pr_review_text(topics) == expected_output
