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
Generate a user-friendly summary of the provided git diff for non-technical stakeholders.  
  
OUTPUT Format:  
{{
    "summary": "<SUMMARY_OF_WORK_DONE>",  
    "details": ["<IMPORTANT_DETAILS>", ...],  
    "todo": ["<TODO_ITEMS>", ...],  
    "future_considerations": ["<THINGS_TO_CONSIDER_IN_FUTURE>", ...],  
    "estimated_time": <ESTIMATED_TIME_IN_HOURS>  
}}

estimated_time: its the range of time you think the above work might have taken for a developer. example "10-15hrs"
details: its list of important changes in human readable term so that anyone can understand how the software has been impacted.
  
Guidelines:  
1. Give a high-level overview of the goal.  
2. Break down changes by file or area.  
3. Explain in plain language, avoiding jargon.  
4. Highlight new features, improvements, bug fixes, or optimizations.  
5. Discuss impacts or benefits to the user or system.  
6. Use examples or analogies for clarity.  
7. Maintain a consistent, readable tone.  
  
PATCH DATA: {PATCH_DATA}  
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
