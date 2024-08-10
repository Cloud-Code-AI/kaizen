from kaizen.helpers.output import create_pr_review_text

PR_COLLAPSIBLE_TEMPLATE = (
    "<details>\n"
    "<summary>Review</summary>\n"
    "<p>\n"
    "<b>Comment:</b>{comment}<br>\n"
    "<b>Reason:</b>{reason}<br>\n"
    "<b>Solution:</b>{solution}<br>\n"
    "<b>Confidence:</b>{confidence}<br>\n"
    "<b>Start Line:</b>{start_line}<br>\n"
    "<b>End Line:</b>{end_line}<br>\n"
    "<b>File Name:</b>{file_name}<br>\n"
    "<b>Severity:</b>{severity}<br>\n"
    "</p>\n"
    "</details>"
)


def test_create_pr_review_text_no_issues():
    topics = {
        "Syntax": [
            {
                "comment": "Good syntax.",
                "reason": "Follows PEP8.",
                "solution": "None needed.",
                "confidence": "high",
                "start_line": 1,
                "end_line": 2,
                "file_name": "file1.py",
                "severity_level": 5,
            }
        ]
    }
    expected_output = (
        "## Code Review\n\n"
        "✅ **All Clear:** This PR is ready to merge! 👍\n\n"
        "### Syntax\n\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="Good syntax.",
            reason="Follows PEP8.",
            solution="None needed.",
            confidence="high",
            start_line=1,
            end_line=2,
            file_name="file1.py",
            severity=5,
        )
        + "\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_with_critical_issue():
    topics = {
        "Security": [
            {
                "comment": "Vulnerability found.",
                "reason": "Potential SQL injection.",
                "solution": "Use parameterized queries.",
                "confidence": "critical",
                "start_line": 10,
                "end_line": 12,
                "file_name": "file2.py",
                "severity_level": 9,
            }
        ]
    }
    expected_output = (
        "## Code Review\n\n"
        "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
        "### Security\n\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="Vulnerability found.",
            reason="Potential SQL injection.",
            solution="Use parameterized queries.",
            confidence="critical",
            start_line=10,
            end_line=12,
            file_name="file2.py",
            severity=9,
        )
        + "\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_empty_topics():
    topics = {}
    expected_output = (
        "## Code Review\n\n" "✅ **All Clear:** This PR is ready to merge! 👍\n\n"
    )
    assert create_pr_review_text(topics) == expected_output


def test_create_pr_review_text_mixed_reviews():
    topics = {
        "Performance": [
            {
                "comment": "Optimize this loop.",
                "reason": "It is too slow.",
                "solution": "Use list comprehension.",
                "confidence": "medium",
                "start_line": 5,
                "end_line": 6,
                "file_name": "file3.py",
                "severity_level": 6,
            },
            {
                "comment": "Critical performance issue.",
                "reason": "Inefficient algorithm.",
                "solution": "Refactor the algorithm.",
                "confidence": "critical",
                "start_line": 15,
                "end_line": 20,
                "file_name": "file3.py",
                "severity_level": 10,
            },
        ],
        "Documentation": [
            {
                "comment": "Add docstrings.",
                "reason": "Missing documentation.",
                "solution": "Add docstrings to all functions.",
                "confidence": "high",
                "start_line": 1,
                "end_line": 1,
                "file_name": "file4.py",
                "severity_level": 3,
            }
        ],
    }
    expected_output = (
        "## Code Review\n\n"
        "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
        "### Performance\n\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="Optimize this loop.",
            reason="It is too slow.",
            solution="Use list comprehension.",
            confidence="medium",
            start_line=5,
            end_line=6,
            file_name="file3.py",
            severity=6,
        )
        + "\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="Critical performance issue.",
            reason="Inefficient algorithm.",
            solution="Refactor the algorithm.",
            confidence="critical",
            start_line=15,
            end_line=20,
            file_name="file3.py",
            severity=10,
        )
        + "\n"
        + "### Documentation\n\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="Add docstrings.",
            reason="Missing documentation.",
            solution="Add docstrings to all functions.",
            confidence="high",
            start_line=1,
            end_line=1,
            file_name="file4.py",
            severity=3,
        )
        + "\n"
    )
    assert create_pr_review_text(topics) == expected_output
