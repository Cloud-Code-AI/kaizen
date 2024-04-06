import logging

logger = logging.getLogger(__name__)


COLLAPSIBLE_TEMPLATE = """
<details>
<summary>{comment}</summary>

### Reason
{reasoning}

### Confidence
{confidence}
</details>
"""


def json_to_markdown(data):
    markdown_output = "## Code Review Feedback\n\n"

    for review in data["review"]:
        markdown_output += f"### {review['topic']}\n\n"
        ct = COLLAPSIBLE_TEMPLATE.format(
            comment=review.get("comment", "NA"),
            reasoning=review.get("reasoning", "NA"),
            confidence=review.get("confidence", "NA"),
        )
        markdown_output += ct + "\n"

    return markdown_output
