import pytest
from kaizen.helpers.output import create_pr_description

DESC_COLLAPSIBLE_TEMPLATE = (
    "<details><summary>Original Description</summary>\n\n{desc}\n\n</details>"
)


@pytest.mark.parametrize(
    "desc, original_desc, expected",
    [
        (
            "New feature added",
            "This is the original description",
            "New feature added\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary>\n\nThis is the original description\n\n</details>",
        ),
        (
            "",
            "",
            "\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary>\n\n\n\n</details>",
        ),
        (
            "Fix bug in code",
            "Original bug description",
            "Fix bug in code\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary>\n\nOriginal bug description\n\n</details>",
        ),
        (
            "Update documentation",
            "",
            "Update documentation\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary>\n\n\n\n</details>",
        ),
    ],
)
def test_create_pr_description(desc, original_desc, expected):
    result = create_pr_description(desc, original_desc)
    assert result == expected


@pytest.mark.parametrize(
    "desc, original_desc",
    [
        (None, "This is the original description"),
        ("New feature added", None),
        (None, None),
    ],
)
def test_create_pr_description_with_none(desc, original_desc):
    with pytest.raises(TypeError):
        create_pr_description(desc, original_desc)


@pytest.mark.parametrize(
    "desc, original_desc, expected_length",
    [("a" * 1000, "b" * 1000, 2024), ("a" * 5000, "b" * 5000, 10024)],
)
def test_create_pr_description_boundary_conditions(
    desc, original_desc, expected_length
):
    result = create_pr_description(desc, original_desc)
    assert len(result) == expected_length


@pytest.mark.parametrize(
    "desc, original_desc, expected",
    [
        (
            "New feature added",
            "This is the original description",
            "New feature added\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary>\n\nThis is the original description\n\n</details>",
        ),
        (
            "",
            "",
            "\n\n> ✨ Generated with love by Kaizen ❤️\n\n<details><summary>Original Description</summary>\n\n\n\n</details>",
        ),
    ],
)
def test_create_pr_description_with_mocked_template(
    desc, original_desc, expected, mocker
):
    mocker.patch(
        "kaizen.helpers.output.DESC_COLLAPSIBLE_TEMPLATE", DESC_COLLAPSIBLE_TEMPLATE
    )
    result = create_pr_description(desc, original_desc)
    assert result == expected
