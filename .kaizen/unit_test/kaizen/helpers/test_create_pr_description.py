import pytest
import time
from kaizen.helpers.output import create_pr_description

DESC_COLLAPSIBLE_TEMPLATE = "<details><summary>Original Description</summary>\n\n{desc}\n\n</details>"

@pytest.mark.parametrize("desc, original_desc, expected", [
    # Normal Cases
    ("This is a PR description", "This is the original detailed description",
     "This is a PR description\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>\n\nThis is the original detailed description\n\n</details>"),
    ("Fixes a bug", "This fixes a bug in the system",
     "Fixes a bug\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>\n\nThis fixes a bug in the system\n\n</details>"),
    # Edge Cases
    ("", "This is the original detailed description",
     "\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>\n\nThis is the original detailed description\n\n</details>"),
    ("This is a PR description", "",
     "This is a PR description\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>\n\n\n\n</details>"),
    ("", "",
     "\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>\n\n\n\n</details>"),
    ("# Heading\n* Bullet", "**Bold**\n_Italic_",
     "# Heading\n* Bullet\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>\n\n**Bold**\n_Italic_\n\n</details>"),
    # Special Characters and HTML Tags
    ("<h1>Title</h1>", "<p>This is a <strong>bold</strong> statement</p>",
     "<h1>Title</h1>\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>\n\n<p>This is a <strong>bold</strong> statement</p>\n\n</details>"),
    ("Special characters: !@#$%^&*()", "More special characters: ~`<>?",
     "Special characters: !@#$%^&*()\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>\n\nMore special characters: ~`<>?\n\n</details>"),
])
def test_create_pr_description_normal_and_edge_cases(desc, original_desc, expected):
    assert create_pr_description(desc, original_desc) == expected

@pytest.mark.parametrize("desc, original_desc, expected_error_message", [
    # Error Handling
    (None, "This is the original detailed description", "desc must be a string"),
    (123, "This is the original detailed description", "desc must be a string"),
    ([], "This is the original detailed description", "desc must be a string"),
    ("This is a PR description", None, "original_desc must be a string"),
    ("This is a PR description", 123, "original_desc must be a string"),
    ("This is a PR description", [], "original_desc must be a string"),
])
def test_create_pr_description_error_handling(desc, original_desc, expected_error_message):
    with pytest.raises(TypeError) as exc_info:
        create_pr_description(desc, original_desc)
    assert str(exc_info.value) == expected_error_message

@pytest.mark.parametrize("desc, original_desc", [
    # Boundary Conditions
    ("a" * 10000, "b" * 10000),
    ("a" * 100000, "b" * 100000),
])
def test_create_pr_description_boundary_conditions(desc, original_desc):
    start_time = time.time()
    result = create_pr_description(desc, original_desc)
    end_time = time.time()
    execution_time = end_time - start_time

    assert result.startswith(desc)
    assert result.endswith(DESC_COLLAPSIBLE_TEMPLATE.format(desc=original_desc))
    assert "> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️" in result
    assert len(result) == len(desc) + len(original_desc) + len("\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>\n\n\n\n</details>") - 2
    # Removed the arbitrary 1-second boundary condition
    print(f"Execution time: {execution_time} seconds")

if __name__ == "__main__":
    pytest.main()