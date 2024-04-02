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

    for category, comments in data["review"].items():
        markdown_output += f"### {category}\n\n"
        if type(comments) == dict:
            COLLAPSIBLE_TEMPLATE.format(
                comment=comments.get("comment", "NA"),
                reasoning=comments.get("reasoning", "NA"),
                confidence=comments.get("confidence", "NA"),
            )
        else:
            for comment in comments:
                markdown_output += f"- {comment}\n"
        markdown_output += "\n"

    # Print the markdown output
    return markdown_output
