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
Synthesize multiple PR descriptions into a single, concise summary. Focus on the most critical information.

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
- Limit to 3-5 bullet points for key changes across all PRs.
- Prioritize the most significant modifications and features.
- Eliminate redundancies and minor details.
- Keep all descriptions concise and actionable.

Analyze the provided PR descriptions and generate a unified, compact summary. Use your judgment to highlight the most important aspects across all changes.

Here is the information:
{DESCS}
"""
