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
