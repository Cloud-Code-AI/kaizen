import pytest
from kaizen.helpers.output import create_pr_description

DESC_COLLAPSIBLE_TEMPLATE = (
    "<details><summary>Original Description</summary>{desc}</details>"
)


@pytest.mark.parametrize(
    "desc, original_desc, expected",
    [
        (
            "This is a PR description.",
            "This is the original description.",
            "This is a PR description.\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary>This is the original description.</details>",
        ),
        (
            "Short desc.",
            "Original.",
            "Short desc.\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary>Original.</details>",
        ),
        (
            "",
            "Empty original.",
            "\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary>Empty original.</details>",
        ),
        (
            "Edge case with special chars !@#$%^&*()",
            "Special chars in original !@#$%^&*()",
            "Edge case with special chars !@#$%^&*()\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary>Special chars in original !@#$%^&*()</details>",
        ),
        (
            "Long description " + "a" * 1000,
            "Long original description " + "b" * 1000,
            "Long description "
            + "a" * 1000
            + "\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary>Long original description "
            + "b" * 1000
            + "</details>",
        ),
    ],
)
def test_create_pr_description(desc, original_desc, expected):
    assert create_pr_description(desc, original_desc) == expected


@pytest.mark.parametrize(
    "desc, original_desc",
    [(None, "Original description"), ("Description", None), (None, None)],
)
def test_create_pr_description_with_none(desc, original_desc):
    with pytest.raises(TypeError):
        create_pr_description(desc, original_desc)


@pytest.mark.parametrize(
    "desc, original_desc, expected",
    [
        (
            "This is a PR description.",
            "",
            "This is a PR description.\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary></details>",
        ),
        (
            "",
            "",
            "\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary></details>",
        ),
    ],
)
def test_create_pr_description_with_empty_original(desc, original_desc, expected):
    assert create_pr_description(desc, original_desc) == expected
