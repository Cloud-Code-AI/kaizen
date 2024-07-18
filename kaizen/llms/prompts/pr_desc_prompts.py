PR_DESCRIPTION_SYSTEM_PROMPT = """
As a senior software developer reviewing code submissions, provide thorough, constructive feedback and suggestions for improvements. Consider best practices, error handling, performance, readability, and maintainability. Offer objective and respectful reviews that help developers enhance their skills and code quality. Use your expertise to provide comprehensive feedback without asking clarifying questions.
"""

PR_DESCRIPTION_PROMPT = """
Summarize the main purpose, scope of changes, significant modifications, refactoring, or new features in this pull request.

Output Format:
```markdown
# {{Generated PR Title}}

## Overview
{{Brief summary of overall purpose}}

## Changes
- Key Changes: {{List main modifications}}
- New Features: {{List key new features}}
- Refactoring: {{List main refactoring changes}}
```

Instructions:
- Create a concise summary of the PR's main purpose.
- Use markdown formatting for readability.
- Focus on significant changes and avoid repetition.

Based on:
Title: {PULL_REQUEST_TITLE}
Description: {PULL_REQUEST_DESC}
Patch:
{CODE_DIFF}

Analyze the information and generate a comprehensive summary. Make reasonable inferences for unclear details based on your development experience.
"""

PR_FILE_DESCRIPTION_PROMPT = """
Summarize the main purpose, scope of changes, significant modifications, refactoring, or new features in this pull request file.

Output Format:
```markdown
# {{Generated PR Title}}

## Overview
{{Brief summary of file changes}}

## Details
- Main Changes: {{List key modifications}}
- New Features: {{List new features, if any}}
- Refactoring: {{List refactoring changes, if any}}
```

Instructions:
- Create a concise summary of the file changes.
- Use markdown formatting for readability.
- Focus on significant changes and avoid repetition.

Based on:
Title: {PULL_REQUEST_TITLE}
Description: {PULL_REQUEST_DESC}
Patch:
{CODE_DIFF}

Analyze the information and generate a comprehensive summary. Make reasonable inferences for unclear details based on your development experience.
"""

MERGE_PR_DESCRIPTION_PROMPT = """
Synthesize multiple PR descriptions into a single, comprehensive summary. Create a markdown-formatted description that captures the main purpose, scope of changes, and significant modifications.

Output Format:
```markdown
# {{Generated PR Title}}

## Overview
{{Brief summary of overall purpose}}

## Changes
- New Features: {{List key new features}}
- Refactoring: {{List main refactoring changes}}
- Other Changes: {{List other significant modifications}}
```

Instructions:
- Capture the essence of all descriptions concisely.
- Use markdown formatting for readability.
- Organize details into the specified sections.
- Focus on the most significant aspects across all descriptions.
- Ensure all unique and important points are included.

Analyze the provided PR descriptions and generate a unified summary. Use your judgment to resolve any contradictions or unclear points.

Here is the information:
{DESCS}
"""
