import pytest
import logging
from cloudcode.helpers.output import PR_COLLAPSIBLE_TEMPLATE, create_pr_review_from_json


@pytest.fixture
def test_data():
    return {
        "review": [
            {
                "topic": "Code Quality",
                "comment": "The code is well-structured and easy to read.",
                "reasoning": "The code follows best practices and coding standards.",
                "confidence": "High",
            },
            {
                "topic": "Performance",
                "comment": "The code could be optimized for better performance.",
                "reasoning": "There are some inefficient loops and data structures used.",
                "confidence": "Medium",
            },
            {
                "topic": "Performance",
                "comment": "The code could be optimized for better performance.",
                "reasoning": "There are some inefficient loops and data structures used.",
                "confidence": "Medium",
            },
            {
                "topic": "Security",
                "comment": "NA",
                "reasoning": "NA",
                "confidence": "NA",
            },
        ]
    }


def test_json_to_markdown(test_data, capfd):
    logging.getLogger().setLevel(logging.ERROR)
    expected_output = "## Code Review Feedback\n\n"
    expected_output += "### Code Quality\n\n"
    expected_output += (
        PR_COLLAPSIBLE_TEMPLATE.format(
            comment="The code is well-structured and easy to read.",
            reasoning="The code follows best practices and coding standards.",
            confidence="High",
        )
        + "\n"
    )
    expected_output += "### Performance\n\n"
    expected_output += (
        PR_COLLAPSIBLE_TEMPLATE.format(
            comment="The code could be optimized for better performance.",
            reasoning="There are some inefficient loops and data structures used.",
            confidence="Medium",
        )
        + "\n"
        + PR_COLLAPSIBLE_TEMPLATE.format(
            comment="The code could be optimized for better performance.",
            reasoning="There are some inefficient loops and data structures used.",
            confidence="Medium",
        )
        + "\n"
    )
    expected_output += "### Security\n\n"
    expected_output += (
        PR_COLLAPSIBLE_TEMPLATE.format(comment="NA", reasoning="NA", confidence="NA")
        + "\n"
    )

    output = create_pr_review_from_json(test_data)
    captured = capfd.readouterr()
    assert output == expected_output
    assert captured.out == ""
