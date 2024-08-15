from typing import Dict, List


def create_pr_review_text(
    reviews: Dict, code_quality: float, tests: List = None
) -> str:

    markdown_output = "# 🔍 Code Review Summary\n\n"

    if sum(1 for review in reviews if review["confidence"] == "critical") == 0:
        markdown_output += "✅ **All Clear:** This commit looks good! 👍\n\n"
    else:
        markdown_output += (
            "❗ **Attention Required:** This push has potential issues. 🚨\n\n"
        )

    # Add Stats section
    markdown_output += create_stats_section(reviews)

    # Add Code Quality section
    if code_quality is not None:
        markdown_output += f"## 🏆 Code Quality\n"
        markdown_output += f"[{'█' * (code_quality // 5)}{'░' * (20 - code_quality // 5)}] {code_quality}% "
        markdown_output += f"({get_quality_label(code_quality)})\n\n"

    # Categorize issues
    categories = {
        "critical": [],
        "important": [],
        "moderate": [],
        "low": [],
        "trivial": [],
    }
    for review in reviews:
        categories[review["confidence"]].append(review)

    # Add issues sections
    for confidence, emoji in [
        ("critical", "🚨"),
        ("important", "🟠"),
    ]:
        issues = categories[confidence]
        if issues:
            markdown_output += f"## {emoji} {confidence.capitalize()} Issues\n\n"
            markdown_output += create_issues_section(issues)

    # Add Test Cases section
    if tests:
        markdown_output += create_test_cases_section()

    # # Add Highlights section
    # markdown_output += "## 👍 Highlights\n"
    # markdown_output += "- Good code organization and structure\n"
    # markdown_output += "- Consistent naming conventions used throughout\n\n"

    # # Add Next Steps section
    # markdown_output += create_next_steps_section()

    # # Add Trends section
    # markdown_output += create_trends_section()

    # Add footer
    markdown_output += "---\n\n"
    markdown_output += (
        "> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️\n\n"
    )
    markdown_output += create_useful_commands_section()

    return markdown_output


def create_stats_section(reviews: List[Dict]) -> str:
    total_issues = len(reviews)
    critical_issues = sum(1 for review in reviews if review["confidence"] == "critical")
    important_issues = sum(
        1 for review in reviews if review["confidence"] == "important"
    )
    minor_issues = sum(
        1 for review in reviews if review["confidence"] not in ["critical", "important"]
    )
    files_affected = len(set(review["file_name"] for review in reviews))

    output = "## 📊 Stats\n"
    output += f"- Total Issues: {total_issues}\n"
    output += f"- Critical: {critical_issues}\n"
    output += f"- Important: {important_issues}\n"
    output += f"- Minor: {minor_issues}\n"
    output += f"- Files Affected: {files_affected}\n"
    return output


def create_issues_section(issues: List[Dict]) -> str:
    output = "<details>\n"
    output += f"<summary><strong>{issues[0]['topic']} ({len(issues)} issues)</strong></summary>\n\n"
    for i, issue in enumerate(issues, 1):
        output += create_issue_section(issue, i)
    output += "</details>\n\n"
    return output


def create_issue_section(issue: Dict, index: int) -> str:
    output = f"### {index}. {issue['comment']}\n"
    output += f"📁 **File:** `{issue['file_name']}:{issue['start_line']}`\n"
    output += f"⚖️ **Severity:** {issue['severity_level']}/10\n"
    output += f"🔍 **Description:** {issue['reason']}\n"
    output += f"💡 **Solution:** {issue['solution']}\n\n"
    output += "**Current Code:**\n"
    output += f"```python\n{issue['actual_code']}\n```\n\n"
    output += "**Suggested Code:**\n"
    output += f"```python\n{issue['fixed_code']}\n```\n\n"
    return output


def create_test_cases_section() -> str:
    return """## 🧪 Test Cases

<details>
<summary><strong>Test Updates Required</strong></summary>

The following test files need to be updated to reflect recent changes:

1. `tests/test_code_review/test_helper.py`
   - Update needed for new error logging in exception handling

2. `tests/test_code_scan/test_views.py`
   - Add test case for JSON parsing error handling
   - Update test case for `update_scan_frequency` function

To automatically create a PR with these test changes, use the command `!unittest` in a comment.

</details>

"""


def create_next_steps_section() -> str:
    return """## 📝 Next Steps
1. Address all Critical issues, particularly focusing on error handling
2. Review and fix the Important issue related to input validation
3. Update test cases to reflect recent changes (use `!unittest` command)
4. Consider improving overall test coverage (currently at 75%)

"""


def create_trends_section() -> str:
    return """## 📈 Trends
- Critical issues: 2 (↑ from avg. 1.5)
- Code Quality: 60% (↓ from last PR 75%)
- Test Coverage: 75% (↓ from last PR 80%)

"""


def get_quality_label(percentage: int) -> str:
    if percentage >= 90:
        return "Excellent"
    elif percentage >= 80:
        return "Good"
    elif percentage >= 70:
        return "Fair"
    elif percentage >= 60:
        return "Needs Improvement"
    else:
        return "Poor"


def create_useful_commands_section() -> str:
    return """<details>
<summary>Useful Commands</summary>

- **Feedback:** Reply with `!feedback [your message]`
- **Ask PR:** Reply with `!ask-pr [your question]`
- **Review:** Reply with `!review`
- **Explain:** Reply with `!explain [issue number]` for more details on a specific issue
- **Ignore:** Reply with `!ignore [issue number]` to mark an issue as false positive
- **Update Tests:** Reply with `!unittest` to create a PR with test changes
</details>
"""
