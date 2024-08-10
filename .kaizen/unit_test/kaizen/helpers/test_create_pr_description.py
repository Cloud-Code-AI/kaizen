Sure, here is a pytest-style unit test file for the `create_pr_description` function:

```python
import pytest
from kaizen.helpers.output import create_pr_description

DESC_COLLAPSIBLE_TEMPLATE = """
<details>
  <summary>Original Description</summary>

  {desc}

</details>
"""

@pytest.mark.parametrize(
    "desc, original_desc, expected_output",
    [
        (
            "This is a PR description",
            "This is the original description",
            "This is a PR description\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" +
            DESC_COLLAPSIBLE_TEMPLATE.format(desc="This is the original description")
        ),
        (
            "",
            "This is the original description",
            "\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" +
            DESC_COLLAPSIBLE_TEMPLATE.format(desc="This is the original description")
        ),
        (
            "This is a PR description",
            "",
            "This is a PR description\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" +
            DESC_COLLAPSIBLE_TEMPLATE.format(desc="")
        ),
        (
            "",
            "",
            "\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" +
            DESC_COLLAPSIBLE_TEMPLATE.format(desc="")
        ),
        (
            "Special characters !@#$%^&*()",
            "Original with special characters !@#$%^&*()",
            "Special characters !@#$%^&*()\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n" +
            DESC_COLLAPSIBLE_TEMPLATE.format(desc="Original with special characters !@#$%^&*()")
        )
    ]
)
def test_create_pr_description(desc, original_desc, expected_output):
    assert create_pr_description(desc, original_desc) == expected_output
```

This test file covers the identified test scenarios using `pytest.mark.parametrize` to handle multiple test cases efficiently. Each test case includes the `desc`, `original_desc`, and the `expected_output` to verify the correctness of the function.