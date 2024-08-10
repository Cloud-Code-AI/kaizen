import pytest
from kaizen.helpers.output import create_pr_description

DESC_COLLAPSIBLE_TEMPLATE = (
    "<details><summary>Original Description</summary>{desc}</details>"
)


@pytest.mark.parametrize(
    "desc, original_desc, expected",
    [
        (
            "This is a test description.",
            "This is the original description.",
            "This is a test description.\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>This is the original description.</details>",
        ),
        (
            "Short desc.",
            "Short original.",
            "Short desc.\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>Short original.</details>",
        ),
        (
            "",
            "Empty original.",
            "\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>Empty original.</details>",
        ),
        (
            "Long description " * 10,
            "Long original description " * 10,
            "Long description Long description Long description Long description Long description Long description Long description Long description Long description Long description \n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>Long original description Long original description Long original description Long original description Long original description Long original description Long original description Long original description Long original description Long original description </details>",
        ),
    ],
)
def test_create_pr_description(desc, original_desc, expected):
    assert create_pr_description(desc, original_desc) == expected


def test_create_pr_description_with_special_characters():
    desc = "Special characters: !@#$%^&*()"
    original_desc = "Original special: <>?/:;\"'[]{}"
    expected = (
        "Special characters: !@#$%^&*()\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>Original special: <>?/:;\"'[]{}"
        "</details>"
    )
    assert create_pr_description(desc, original_desc) == expected


def test_create_pr_description_with_empty_strings():
    desc = ""
    original_desc = ""
    expected = (
        "\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>"
        "</details>"
    )
    assert create_pr_description(desc, original_desc) == expected


def test_create_pr_description_with_whitespace_strings():
    desc = "    "
    original_desc = "    "
    expected = (
        "    \n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n<details><summary>Original Description</summary>    "
        "</details>"
    )
    assert create_pr_description(desc, original_desc) == expected
