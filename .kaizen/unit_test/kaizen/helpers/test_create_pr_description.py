import pytest
from kaizen.helpers.output import create_pr_description

DESC_COLLAPSIBLE_TEMPLATE = """
<details>
  <summary>Original Description</summary>

  {desc}

</details>
"""

@pytest.mark.parametrize("desc, original_desc, expected", [
    # Normal Cases
    ("This is a PR description", "Original description", 
     "This is a PR description\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" + DESC_COLLAPSIBLE_TEMPLATE.format(desc="Original description")),

    # Edge Cases
    ("", "Original description", 
     "\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" + DESC_COLLAPSIBLE_TEMPLATE.format(desc="Original description")),
    ("This is a PR description", "", 
     "This is a PR description\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" + DESC_COLLAPSIBLE_TEMPLATE.format(desc="")),
    ("", "", 
     "\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" + DESC_COLLAPSIBLE_TEMPLATE.format(desc="")),
    ("This is a PR description with **bold** and _italic_ text", "Original description with **bold** and _italic_ text", 
     "This is a PR description with **bold** and _italic_ text\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" + DESC_COLLAPSIBLE_TEMPLATE.format(desc="Original description with **bold** and _italic_ text")),
    ("This is a PR description", "Original description with **bold** and _italic_ text", 
     "This is a PR description\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" + DESC_COLLAPSIBLE_TEMPLATE.format(desc="Original description with **bold** and _italic_ text")),

    # Error Handling
    (None, "Original description", TypeError),
    ("This is a PR description", None, TypeError),
    (None, None, TypeError),

    # Boundary Conditions
    ("a" * 10000, "Original description", 
     "a" * 10000 + "\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" + DESC_COLLAPSIBLE_TEMPLATE.format(desc="Original description")),
    ("This is a PR description", "b" * 10000, 
     "This is a PR description\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" + DESC_COLLAPSIBLE_TEMPLATE.format(desc="b" * 10000)),
    ("a" * 10000, "b" * 10000, 
     "a" * 10000 + "\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" + DESC_COLLAPSIBLE_TEMPLATE.format(desc="b" * 10000)),
])
def test_create_pr_description(desc, original_desc, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            create_pr_description(desc, original_desc)
    else:
        assert create_pr_description(desc, original_desc) == expected