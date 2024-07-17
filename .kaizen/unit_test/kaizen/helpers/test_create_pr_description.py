import pytest
from kaizen.helpers.output import create_pr_description

DESC_COLLAPSIBLE_TEMPLATE = "<details><summary>Original Description</summary>{desc}</details>"

def test_create_pr_description_normal_case():
    desc = "This is a pull request description."
    original_desc = "This is the original description."
    expected_output = (
        "This is a pull request description.\n\n> ✨ Generated with love by Kaizen ❤️\n\n"
        "<details><summary>Original Description</summary>This is the original description.</details>"
    )
    assert create_pr_description(desc, original_desc) == expected_output

def test_create_pr_description_empty_desc():
    desc = ""
    original_desc = "This is the original description."
    expected_output = (
        "\n\n> ✨ Generated with love by Kaizen ❤️\n\n"
        "<details><summary>Original Description</summary>This is the original description.</details>"
    )
    assert create_pr_description(desc, original_desc) == expected_output

def test_create_pr_description_empty_original_desc():
    desc = "This is a pull request description."
    original_desc = ""
    expected_output = (
        "This is a pull request description.\n\n> ✨ Generated with love by Kaizen ❤️\n\n"
        "<details><summary>Original Description</summary></details>"
    )
    assert create_pr_description(desc, original_desc) == expected_output

def test_create_pr_description_both_empty():
    desc = ""
    original_desc = ""
    expected_output = (
        "\n\n> ✨ Generated with love by Kaizen ❤️\n\n"
        "<details><summary>Original Description</summary></details>"
    )
    assert create_pr_description(desc, original_desc) == expected_output

def test_create_pr_description_long_desc():
    desc = "a" * 1000
    original_desc = "b" * 1000
    expected_output = (
        "a" * 1000 + "\n\n> ✨ Generated with love by Kaizen ❤️\n\n"
        "<details><summary>Original Description</summary>" + "b" * 1000 + "</details>"
    )
    assert create_pr_description(desc, original_desc) == expected_output