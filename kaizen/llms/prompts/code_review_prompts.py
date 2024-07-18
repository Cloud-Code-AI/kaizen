CODE_REVIEW_SYSTEM_PROMPT = """
As a senior software developer reviewing code submissions, provide thorough, constructive feedback and suggestions for improvements. Consider best practices, error handling, performance, readability, and maintainability. Offer objective and respectful reviews that help developers enhance their skills and code quality. Use your expertise to provide comprehensive feedback without asking clarifying questions.
"""

CODE_REVIEW_PROMPT = """
As an experienced software engineer, provide a concise, actionable code review for the given pull request. Evaluate code changes, identify potential issues, and offer constructive feedback.

Generate a JSON object with the following structure, including only sections with relevant feedback:
{{
  "review": [
    {{
      "topic": "<SECTION_TOPIC>",
      "comment": "<CONCISE_ISSUE_DESCRIPTION>",
      "confidence": "critical|important|moderate|low|trivial",
      "reason": "<ISSUE_REASONING>",
      "solution": "<HIGH_LEVEL_SOLUTION>",
      "fixed_code": "<CORRECTED_CODE>",
      "start_line": <START_LINE_NUMBER>,
      "end_line": <END_LINE_NUMBER>,
      "side": "LEFT|RIGHT",
      "file_name": "<FULL_FILE_PATH>",
      "sentiment": "positive|negative|neutral",
      "severity_level": <1_TO_10>
    }}
  ]
}}
Guidelines:

Provide actionable feedback with specific file paths and line numbers
Use markdown for code snippets
Merge duplicate feedback
Concise yet useful comments
Examine: syntax/logic errors, loops, null values, resource leaks, race conditions, integration/performance issues, security vulnerabilities
If no feedback: {{"review": []}}

Field Guidelines:
- "fixed_code": Generate corrected code to replace the commented lines, ensuring changes are between start_line and end_line.
- "start_line": The actual line number in the new file where the change begins. For added lines, this is the line number of the first '+' line in the chunk.
- "end_line": The actual line number in the new file where the change ends. For added lines, this is the line number of the last '+' line in the chunk.
- "side": Use "LEFT" for deleted lines, "RIGHT" for added lines (for GitHub review comments).
- "file_name": Include the full file path for precise issue location.
- "severity_level": Score from 1 (least severe) to 10 (most critical).

Patch Data Processing:

Git patch data consists of file information, chunk headers ("@@"), and content changes ('+' for additions, '-' for deletions). Unchanged lines provide context. Multiple chunks may exist per file.

Key points:
1. Changes can occur in multiple files
2. A file may have multiple change chunks
3. Line numbers in later chunks are affected by earlier changes
4. Calculate actual line numbers in the new version, accounting for all previous changes

Interpreting a diff hunk:
1. Hunk header ("@@"): Shows affected line numbers in old and new versions
2. Unchanged lines: No prefix, present in both versions
3. Removed lines: Start with "-"
4. Added lines: Start with "+" (exclude file headers "+++")

Example:
```
@@ -82,7 +82,7 @@ def *retrieve*igd_profile(url):
     Retrieve the device's UPnP profile.
     try:
-        return urllib2.urlopen(url.geturl(), timeout=5).read()
+        return urllib2.urlopen(url.geturl(), timeout=5).read().decode('utf-8')
     except socket.error:
         raise IGDError('IGD profile query timed out')
```

To interpret:
1. Examine hunk header for context
2. Identify removed lines ("-")
3. Identify added lines ("+")
4. Compare changes
5. Use unchanged lines for context

INFORMATION:

Pull Request Title: {PULL_REQUEST_TITLE}
Pull Request Description: {PULL_REQUEST_DESC}

PATCH DATA:
```{CODE_DIFF}```
"""

FILE_CODE_REVIEW_PROMPT = """
As an experienced software engineer, provide a concise, actionable code review for the given pull request. Evaluate code changes, identify potential issues, and offer constructive feedback.

Generate a JSON object with the following structure, including only sections with relevant feedback:
{{
  "review": [
    {{
      "topic": "<SECTION_TOPIC>",
      "comment": "<CONCISE_ISSUE_DESCRIPTION>",
      "confidence": "critical|important|moderate|low|trivial",
      "reason": "<ISSUE_REASONING>",
      "solution": "<HIGH_LEVEL_SOLUTION>",
      "fixed_code": "<CORRECTED_CODE>",
      "start_line": <START_LINE_NUMBER>,
      "end_line": <END_LINE_NUMBER>,
      "side": "LEFT|RIGHT",
      "file_name": "<FULL_FILE_PATH>",
      "sentiment": "positive|negative|neutral",
      "severity_level": <1_TO_10>
    }}
  ]
}}
Guidelines:

Provide actionable feedback with specific file paths and line numbers
Use markdown for code snippets
Merge duplicate feedback
Concise yet useful comments
Examine: syntax/logic errors, loops, null values, resource leaks, race conditions, integration/performance issues, security vulnerabilities
If no feedback: {{"review": []}}

Field Guidelines:
- "fixed_code": Generate corrected code to replace the commented lines, ensuring changes are between start_line and end_line.
- "start_line": The actual line number in the new file where the change begins. For added lines, this is the line number of the first '+' line in the chunk.
- "end_line": The actual line number in the new file where the change ends. For added lines, this is the line number of the last '+' line in the chunk.
- "side": Use "LEFT" for deleted lines, "RIGHT" for added lines (for GitHub review comments).
- "file_name": Include the full file path for precise issue location.
- "severity_level": Score from 1 (least severe) to 10 (most critical).

Patch Data Processing:

Git patch data consists of file information, chunk headers ("@@"), and content changes ('+' for additions, '-' for deletions). Unchanged lines provide context. Multiple chunks may exist per file.

Key points:
1. Changes can occur in multiple files
2. A file may have multiple change chunks
3. Line numbers in later chunks are affected by earlier changes
4. Calculate actual line numbers in the new version, accounting for all previous changes

Interpreting a diff hunk:
1. Hunk header ("@@"): Shows affected line numbers in old and new versions
2. Unchanged lines: No prefix, present in both versions
3. Removed lines: Start with "-"
4. Added lines: Start with "+" (exclude file headers "+++")

Example:
```
@@ -82,7 +82,7 @@ def *retrieve*igd_profile(url):
     Retrieve the device's UPnP profile.
     try:
-        return urllib2.urlopen(url.geturl(), timeout=5).read()
+        return urllib2.urlopen(url.geturl(), timeout=5).read().decode('utf-8')
     except socket.error:
         raise IGDError('IGD profile query timed out')
```

To interpret:
1. Examine hunk header for context
2. Identify removed lines ("-")
3. Identify added lines ("+")
4. Compare changes
5. Use unchanged lines for context

INFORMATION:

Pull Request Title: {PULL_REQUEST_TITLE}
Pull Request Description: {PULL_REQUEST_DESC}

File PATCH:
```{FILE_PATCH}```
"""

PR_DESCRIPTION_PROMPT = """
As a skilled developer reviewing a pull request, generate a concise and well-formatted description summarizing the main purpose, scope of changes, significant modifications, refactoring, or new features introduced in the pull request.

Provide the output in the following JSON format:

{{
  "desc": "
### Summary

<Brief one-line summary of the pull request>

### Details

<Detailed multi-line description in markdown format>
- List of key changes
- New features
- Refactoring details
  "
}}

When generating the description:

- Create a concise and clear summary highlighting the main purpose of the pull request.
- Use markdown formatting in the detailed description for better readability.
- Organize the details into relevant sections or bullet points.
- Focus on the most significant aspects of the changes.
- Avoid repeating information already present in the pull request title or description.
- Ensure the output is in valid JSON format.

Based on the provided information:

Pull Request Title: {PULL_REQUEST_TITLE}
Pull Request Description: {PULL_REQUEST_DESC}
Patch Data:
{CODE_DIFF}

Analyze the information thoroughly and generate a comprehensive summary and detailed description.
Use your expertise to identify and highlight the most important aspects of the changes without asking for additional clarification. If certain details are unclear, make reasonable inferences based on the available information and your development experience.

"""

PR_FILE_DESCRIPTION_PROMPT = """
As a skilled developer reviewing a pull request, generate a concise and well-formatted description summarizing the main purpose, scope of changes, significant modifications, refactoring, or new features introduced in the pull request.

Provide the output in the following JSON format:

{{
  "desc": "
### Summary

<Brief one-line summary of the pull request>

### Details

<Detailed multi-line description in markdown format>
- List of key changes
- New features
- Refactoring details
  "
}}

When generating the description:

- Create a concise and clear summary highlighting the main purpose of the pull request.
- Use markdown formatting in the detailed description for better readability.
- Organize the details into relevant sections or bullet points.
- Focus on the most significant aspects of the changes.
- Avoid repeating information already present in the pull request title or description.
- Ensure the output is in valid JSON format.

Based on the provided information:

Pull Request Title: {PULL_REQUEST_TITLE}
Pull Request Description: {PULL_REQUEST_DESC}
Patch Data:
{CODE_DIFF}

Analyze the information thoroughly and generate a comprehensive summary and detailed description.
Use your expertise to identify and highlight the most important aspects of the changes without asking for additional clarification. If certain details are unclear, make reasonable inferences based on the available information and your development experience.
"""

MERGE_PR_DESCRIPTION_PROMPT = """
As a skilled developer reviewing a pull request, generate a concise and well-formatted description that synthesizes multiple PR descriptions into a single, comprehensive summary. This summary should encapsulate the main purpose, scope of changes, significant modifications, refactoring, and new features introduced in the pull request.

Using the provided PR descriptions in JSON format, create a merged PR Description in the following JSON format:

{{
  "desc": "
### Summary

<Brief one-line summary encompassing the overall purpose of the pull request>

### Details

<Detailed multi-line description in markdown format>
- Consolidated list of key changes
- Aggregated new features
- Combined refactoring details
- Other significant aspects from all descriptions
  "
}}

When generating the merged description:

- Create a concise yet comprehensive summary that captures the essence of all provided descriptions.
- Use markdown formatting in the detailed description for improved readability.
- Organize the details into relevant sections or bullet points, consolidating similar information from different descriptions.
- Focus on the most significant aspects of the changes across all descriptions.
- Eliminate redundancies and repetitions while ensuring all unique and important points are included.
- Ensure the output is in valid JSON format.

Analyze the provided PR descriptions thoroughly and generate a unified, comprehensive summary and detailed description. Use your expertise to identify, merge, and highlight the most important aspects of the changes across all descriptions. If certain details seem contradictory or unclear, use your best judgment to provide the most accurate and coherent representation of the pull request's purpose and changes.

Here is the information:
{DESCS}
"""

PR_DESC_EVALUATION_PROMPT = """
Please evaluate the accuracy and completeness of your previous responses in this conversation.
Identify any potential errors or areas for improvement.

Respond the JSON output as:
{{
  "desc": "
### Summary

<Brief one-line summary encompassing the overall purpose of the pull request>

### Details

<Detailed multi-line description in markdown format>
- Consolidated list of key changes
- Aggregated new features
- Combined refactoring details
- Other significant aspects from all descriptions
  "
}}

"""


PR_REVIEW_EVALUATION_PROMPT = """
Please evaluate the accuracy and completeness of your previous responses in this conversation.
Fix any potential errors or areas for improvement.

Generate a JSON object with the following structure, including only sections with relevant feedback:
{{
  "review": [
    {{
      "topic": "<SECTION_TOPIC>",
      "comment": "<CONSICE_COMMENT_ON_WHATS_THE_ISSUE>",
      "confidence": "<CONFIDENCE_LEVEL>",
      "reason": "<YOUR_REASON_FOR_COMMENTING_THIS_ISSUE>"
      "solution": "<HIGH_LEVEL_SOLUTION>",
      "fixed_code": "<FIXED_CODE>",
      "start_line": "<CODE_START_LINE_INTEGER>",
      "end_line": "<CODE_END_LINE_INTEGER>",
      "side": "<LEFT_OR_RIGHT>",
      "file_name": "<FULL_FILE_PATH>",
      "sentiment": "<COMMENT_SENTIMENT_POSITIVE_NEGATIVE_OR_NEUTRAL>",
      "severity_level": <INTEGER_FROM_1_TO_10>
    }},
    ...
  ]
  }}

Field Guidelines:
- "solution": Provide a high-level solution to the identified issue.
- "fixed_code": Generate corrected code to replace the commented lines, ensuring changes are between start_line and end_line.
- "start_line": The actual line number in the new file where the change begins. For added lines, this is the line number of the first '+' line in the chunk.
- "end_line": The actual line number in the new file where the change ends. For added lines, this is the line number of the last '+' line in the chunk.
- "side": Use "LEFT" for deleted lines, "RIGHT" for added lines (for GitHub review comments).
- "file_name": Include the full file path for precise issue location.
- "severity_level": Score from 1 (least severe) to 10 (most critical).
Confidence Levels based on severity of the issue:
[
  "critical",
  "important",
  "moderate",
  "low",
  "trivial"
]

If no feedback is necessary, return: {{"review": []}}


ACTUAL_PROMPT:
{ACTUAL_PROMPT}

LLM_OUTPUT:
{LLM_OUTPUT}
"""
