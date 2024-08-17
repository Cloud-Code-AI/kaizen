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

<details>
```

Instructions:
- Create a concise yet comprehensive summary of the PR's main purpose.
- Use only the markdown sections specified in the output format.
- Focus on significant changes, avoiding repetition and minor details.
- Ensure all key modifications, new features, and refactoring are captured within the existing sections.
- Keep descriptions brief but informative.
- Do not introduce any new sections or categories beyond those specified.

Patch:
{CODE_DIFF}

Analyze the information and generate a comprehensive summary. Make reasonable inferences for unclear details based on your development experience.
"""

PR_FILE_DESCRIPTION_PROMPT = """
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

<details>
```

Instructions:
- Create a concise yet comprehensive summary of the PR's main purpose.
- Use only the markdown sections specified in the output format.
- Focus on significant changes, avoiding repetition and minor details.
- Ensure all key modifications, new features, and refactoring are captured within the existing sections.
- Keep descriptions brief but informative.
- Do not introduce any new sections or categories beyond those specified.

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
- Key Changes: {{List main modifications}}
- New Features: {{List key new features}}
- Refactoring: {{List main refactoring changes}}

<details>
```

Instructions:
- Create a concise yet comprehensive summary of the PR's main purpose.
- Use only the markdown sections specified in the output format.
- Focus on significant changes, avoiding repetition and minor details.
- Ensure all key modifications, new features, and refactoring are captured within the existing sections.
- Keep descriptions brief but informative.
- Do not introduce any new sections or categories beyond those specified.

Analyze the provided PR descriptions and generate a unified summary. Use your judgment to resolve any contradictions or unclear points.

Here is the information:
{DESCS}
"""
