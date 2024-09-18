WORK_SUMMARY_SYSTEM_PROMPT = """
You are an AI assistant that explains technical code changes in a user-friendly manner to non-technical audiences. Given a git diff:

- Identify key changes (features, bug fixes, optimizations, refactoring).
- Divide changes by specific code areas/files.
- Provide plain language summaries explaining the purpose and goals.
- Use simple language, avoiding excessive jargon.
- Highlight impacts on user experience or the overall system.
- Use examples and analogies for better understanding.
- Maintain a consistent, readable tone and structure.
- Rely solely on the provided diff, without using external resources.
- Avoid making up information; base explanations only on the provided diff.

Your role is to communicate technical work effectively to non-technical stakeholders.
"""

WORK_SUMMARY_PROMPT = """  
Generate a concise summary of the provided git diff for daily/weekly standup reports.  
  
OUTPUT Format:  
{{
    "summary": "<BRIEF_SUMMARY_OF_WORK_DONE>",  
    "details": ["<COMPLETED_TASK>", ...],
    "in_progress": ["<IN_PROGRESS_TASK>", ...],
    "blockers": ["<BLOCKER>", ...],
    "future_considerations": ["<NEXT_STEP>", ...],
    "estimated_time": "<ESTIMATED_TIME_IN_HOURS>"
}}

estimated_time_spent: Range of time spent on the work in hours, e.g., "5-7hrs"
completed_tasks: List of tasks completed, described concisely
in_progress: List of tasks currently being worked on
blockers: Any issues or dependencies preventing progress
next_steps: Immediate next actions or tasks to be tackled
  
Guidelines:  
1. Provide a brief overview of the work done.
2. Focus on key accomplishments and progress.
3. Highlight any challenges or blockers encountered.
4. Keep descriptions concise and relevant to team updates.
5. Avoid technical jargon where possible.
6. Keep summaries concise and to the point.
7. All the points should be in human readable term.
8. Output should be in JSON format.
  
PATCH DATA: {PATCH_DATA}  
"""

MERGE_WORK_SUMMARY_PROMPT = """  
Merge all this information into a consolidated standup report format.

OUTPUT Format:  
{{
    "summary": "<BRIEF_SUMMARY_OF_WORK_DONE>",  
    "details": ["<COMPLETED_TASK>", ...],
    "in_progress": ["<IN_PROGRESS_TASK>", ...],
    "blockers": ["<BLOCKER>", ...],
    "future_considerations": ["<NEXT_STEP>", ...],
    "estimated_time": "<ESTIMATED_TIME_IN_HOURS>"
}}

estimated_time_spent: Range of time spent on the work in hours, e.g., "5-7hrs"
completed_tasks: List of tasks completed, described concisely
in_progress: List of tasks currently being worked on
blockers: Any issues or dependencies preventing progress
next_steps: Immediate next actions or tasks to be tackled
  
Guidelines:  
1. Provide a brief overview of the work done.
2. Focus on key accomplishments and progress.
3. Highlight any challenges or blockers encountered.
4. Keep descriptions concise and relevant to team updates.
5. Avoid technical jargon where possible.
6. Keep summaries concise and to the point.
7. All the points should be in human readable term.
8. Output should be in JSON format.
  
All the summaries: 

{SUMMARY_JSON}
"""

TWITTER_POST_PROMPT = """
Given the following work summary, create a concise and engaging Twitter post (max 280 characters) that highlights the key changes or improvements. Format the post as markdown, enclosed in triple backticks:

Summary:
{SUMMARY}

Twitter Post:
```
<Your Twitter post here>
```
"""

LINKEDIN_POST_PROMPT = """
Based on the following work summary, create a professional LinkedIn post that describes the recent updates or improvements. The post should be more detailed than a Twitter post but still concise and engaging. Format the post as markdown, enclosed in triple backticks:

Summary:
{SUMMARY}

LinkedIn Post:
```
<Your LinkedIn post here>
```
"""
