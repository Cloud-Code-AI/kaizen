def json_to_markdown(data):
    markdown_output = "## Code Review Feedback\n\n"

    for category, comments in data["review"].items():
        markdown_output += f"### {category}\n\n"
        for comment in comments:
            markdown_output += f"- {comment}\n"
        markdown_output += "\n"

    # Print the markdown output
    return markdown_output
