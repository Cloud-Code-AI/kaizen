import pytest
from unittest.mock import patch
from unittest.mock import patch
import logging
from cloudcode.helpers.output import (
    COLLAPSIBLE_TEMPLATE,
    json_to_markdown
)


@pytest.fixture
def test_data():
    return {
        "review": [
            {
                "topic": "Code Quality",
                "comment": "The code is well-structured and easy to read.",
                "reasoning": "The code follows best practices and coding standards.",
                "confidence": "High"
            },
            {
                "topic": "Performance",
                "comment": "The code could be optimized for better performance.",
                "reasoning": "There are some inefficient loops and data structures used.",
                "confidence": "Medium"
            },
            {
                "topic": "Security",
                "comment": "NA",
                "reasoning": "NA",
                "confidence": "NA"
            }
        ]
    }

def test_json_to_markdown(test_data, capfd):
    logging.getLogger().setLevel(logging.ERROR)
    expected_output = "## Code Review Feedback\n\n"
    expected_output += "### Code Quality\n\n"
    expected_output += COLLAPSIBLE_TEMPLATE.format(
        comment="The code is well-structured and easy to read.",
        reasoning="The code follows best practices and coding standards.",
        confidence="High"
    ) + "\n"
    expected_output += "### Performance\n\n"
    expected_output += COLLAPSIBLE_TEMPLATE.format(
        comment="The code could be optimized for better performance.",
        reasoning="There are some inefficient loops and data structures used.",
        confidence="Medium"
    ) + "\n"
    expected_output += "### Security\n\n"
    expected_output += COLLAPSIBLE_TEMPLATE.format(
        comment="NA",
        reasoning="NA",
        confidence="NA"
    ) + "\n"

    output = json_to_markdown(test_data)
    captured = capfd.readouterr()
    assert output == expected_output
    assert captured.out == ""