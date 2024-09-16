PR_DESCRIPTION_SYSTEM_PROMPT = """
As a senior software developer, provide concise, actionable feedback on code submissions. Focus on critical issues and key improvements.
"""

PR_DESCRIPTION_PROMPT = """
Summarize the core purpose and key changes in this pull request.

Output Format:
```markdown
# {{Brief PR Title}}

- Purpose: {{One-sentence summary}}
- Key Changes:
  - {{Bullet points of main modifications}}
- Impact: {{One-sentence on potential effects}}
```

Instructions:
- Create a brief, focused summary.
- Limit to 3-5 bullet points for key changes.
- Omit minor details and focus on significant modifications.
- Keep all descriptions short and to the point.

Patch:
{CODE_DIFF}

Analyze the information and generate a concise summary based on the most important aspects of the changes.
"""

MERGE_PR_DESCRIPTION_PROMPT = """
Merge multiple PR descriptions into a single, comprehensive summary. Focus on the most critical information.

Output Format:
```markdown
# {{Brief, Overarching PR Title}}

- Purpose: {{One-sentence summary encompassing all changes}}
- Key Changes:
  - {{Bullet points of main modifications across all PRs}}
- Impact: {{One-sentence on overall potential effects}}
```

Instructions:
- Create a brief, focused summary that encapsulates all PRs.
- Limit to max 10 bullet points for key changes across all PRs.
- Prioritize the most significant modifications and features.
- Eliminate redundancies and minor details.
- Keep all descriptions concise and actionable.

Analyze the provided PR descriptions and generate a unified, compact summary. Use your judgment to highlight the most important aspects across all changes.

Here is list of PR descriptions in json format:
{DESCS}
"""


PR_COMMIT_MESSAGE_PROMPT = """
Generate a concise and informative Git commit message based on the following description of code changes.
Follow the Conventional Commits format and these best practices:

1. Start with a type prefix, followed by a colon and space (e.g., feat:, fix:, docs:)
2. Use lowercase for the entire subject line
3. Keep the subject line (first line) under 50 characters
4. Summarize the main change in the subject line
5. Leave a blank line between the subject and the body (if a body is needed)
6. Use the body to explain the what and why of the change, not the how
7. Wrap the body at 72 characters
8. Use bullet points in the body for multiple changes if necessary
9. Include relevant issue numbers (e.g., "fixes #123" or "relates to #456")

Common type prefixes:
- feat: A new feature
- fix: A bug fix
- docs: Documentation only changes
- style: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- refactor: A code change that neither fixes a bug nor adds a feature
- perf: A code change that improves performance
- test: Adding missing tests or correcting existing tests
- chore: Changes to the build process or auxiliary tools and libraries

Examples:

1. Simple change:
{{
    "subject": "fix: typo in README.md",
    "body": null
}}

2. Complex change:
{{
    "subject": "feat: user authentication feature",
    "body": "Implement login and logout functionality for users.\\n\\n- Create login form and handle submission\\n- Set up session management\\n- Add logout button and route\\n- Update navbar to show login status\\n\\nRelates to #42"
}}


Based on this description, generate a commit message following the above guidelines and examples. 
If the changes are simple, a subject line alone may suffice. For more complex changes, include a body with additional details.

Provide the output in JSON format with the following structure:
```
{{
    "subject": "prefix:the commit message subject line",
    "body": "The commit message body (if necessary, otherwise null)"
}}
```

Code change description:
{DESC}
"""
