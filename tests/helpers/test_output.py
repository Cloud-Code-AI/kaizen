import pytest


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


# def test_json_to_markdown(test_data, capfd):
#     logging.getLogger().setLevel(logging.ERROR)
#     expected_output = "## Code Review Feedback\n\n"
#     expected_output += "### Code Quality\n\n"
#     expected_output += (
#         PR_COLLAPSIBLE_TEMPLATE.format(
#             comment="The code is well-structured and easy to read.",
#             reasoning="The code follows best practices and coding standards.",
#             confidence="High",
#             file_name="NA",
#             start_line="NA",
#             end_line="NA",
#         )
#         + "\n"
#     )
#     expected_output += "### Performance\n\n"
#     expected_output += (
#         PR_COLLAPSIBLE_TEMPLATE.format(
#             comment="The code could be optimized for better performance.",
#             reasoning="There are some inefficient loops and data structures used.",
#             confidence="Medium",
#             file_name="NA",
#             start_line="NA",
#             end_line="NA",
#         )
#         + "\n"
#         + PR_COLLAPSIBLE_TEMPLATE.format(
#             comment="The code could be optimized for better performance.",
#             reasoning="There are some inefficient loops and data structures used.",
#             confidence="Medium",
#             file_name="NA",
#             start_line="NA",
#             end_line="NA",
#         )
#         + "\n"
#     )
#     expected_output += "### Security\n\n"
#     expected_output += (
#         PR_COLLAPSIBLE_TEMPLATE.format(
#             comment="NA",
#             reasoning="NA",
#             confidence="NA",
#             file_name="NA",
#             start_line="NA",
#             end_line="NA",
#         )
#         + "\n"
#     )

#     reviewer = CodeReviewer()
#     output = reviewer.merge_topics(test_data["review"])
#     text = reviewer.create_pr_review_text(output)
#     captured = capfd.readouterr()
#     assert text == expected_output
#     assert captured.out == ""
