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
  ],
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

Field Guidelines:
- "solution": Provide a high-level solution to the identified issue.
- "fixed_code": Generate corrected code to replace the commented lines, ensuring changes are between start_line and end_line.
- "start_line": The actual line number in the new file where the change begins. For added lines, this is the line number of the first '+' line in the chunk.
- "end_line": The actual line number in the new file where the change ends. For added lines, this is the line number of the last '+' line in the chunk.
- "side": Use "LEFT" for deleted lines, "RIGHT" for added lines (for GitHub review comments).
- "file_name": Include the full file path for precise issue location.
- "severity_level": Score from 1 (least severe) to 10 (most critical).

Patch Data Processing:
Reading git patch data involves understanding several key elements. The patch starts with file information, indicating which files are being modified.
Chunk headers, beginning with "@@", show the affected line numbers in both old and new versions of the file. 
Content changes are marked with '-' for deletions and '+' for additions, while unchanged lines serve as context. 
A single file may have multiple chunks, each starting with a new "@@" header. When calculating line numbers, it's crucial to account for all previous additions and deletions in the file.


When analyzing this patch:
1. Note that there are changes in two different files.
2. The first file has two separate chunks of changes.
3. Line numbers in the second chunk of the first file are affected by the additions in the first chunk.
4. The second file has one chunk of changes, including both additions and a deletion.

Always calculate the actual line numbers in the new version of each file, accounting for all additions and deletions in previous chunks.

Patch Data Processing:
- Identify lines starting with '+' as additions (exclude file header lines starting with '+++').

Confidence Levels: ["critical", "important", "moderate", "low", "trivial"]

Potential Topics:
- Code Quality
- Performance
- Potential Issues
- Improvements

Key Areas to Examine:
- Syntax Errors
- Logic Errors
- Off-by-one Errors
- Infinite Loops
- Null/Undefined Values
- Resource Leaks
- Race Conditions
- Integration Issues
- Performance Issues
- Security Vulnerabilities


Provide actionable feedback, referencing specific files and line numbers. Use markdown code blocks for relevant snippets. Merge duplicate feedback for the same line. Ensure comments are concise yet useful.

If no feedback is necessary, return: {{"review": []}}

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

Patch Data Processing:
Reading git patch data involves understanding several key elements. The patch starts with file information, indicating which files are being modified.
Chunk headers, beginning with "@@", show the affected line numbers in both old and new versions of the file. 
Content changes are marked with '-' for deletions and '+' for additions, while unchanged lines serve as context. 
A single file may have multiple chunks, each starting with a new "@@" header. When calculating line numbers, it's crucial to account for all previous additions and deletions in the file.


When analyzing this patch:
1. Note that there are changes in two different files.
2. The first file has two separate chunks of changes.
3. Line numbers in the second chunk of the first file are affected by the additions in the first chunk.
4. The second file has one chunk of changes, including both additions and a deletion.

Always calculate the actual line numbers in the new version of each file, accounting for all additions and deletions in previous chunks.

Confidence Levels: ["critical", "important", "moderate", "low", "trivial"]

Potential Topics:
- Code Quality
- Performance
- Potential Issues
- Improvements

Key Areas to Examine:
- Syntax Errors
- Logic Errors
- Off-by-one Errors
- Infinite Loops
- Null/Undefined Values
- Resource Leaks
- Race Conditions
- Integration Issues
- Performance Issues
- Security Vulnerabilities


Provide actionable feedback, referencing specific files and line numbers. Use markdown code blocks for relevant snippets. Merge duplicate feedback for the same line. Ensure comments are concise yet useful.

If no feedback is necessary, return: {{"review": []}}

INFORMATION:

Pull Request Title: {PULL_REQUEST_TITLE}
Pull Request Description: {PULL_REQUEST_DESC}

File PATCH:
```{FILE_PATCH}```
"""

PR_DESCRIPTION_PROMPT = """
Summarize this pull request concisely and comprehensively. Output in this markdown format:

```markdown
# Pull Request Summary

## Overview
[One-line summary]

## Key Changes
- [Change 1]
- [Change 2]

## New Features
- [Feature 1]
- [Feature 2]

## Refactoring
- [Refactoring 1]
- [Refactoring 2]

## Notes
[Additional context]
```

Guidelines:
- Highlight main purpose and significant changes
- Use bullet points for clarity
- Avoid repeating PR title/description
- Infer details from available information if needed

Based on:
Title: {PULL_REQUEST_TITLE}
Description: {PULL_REQUEST_DESC}
Patch:
{CODE_DIFF}
"""

PR_FILE_DESCRIPTION_PROMPT = """
Summarize this pull request file concisely and comprehensively. Output in this markdown format:

```markdown
# Pull Request Summary

## Overview
[One-line summary]

## Key Changes
- [Change 1]
- [Change 2]

## New Features
- [Feature 1]
- [Feature 2]

## Refactoring
- [Refactoring 1]
- [Refactoring 2]

## Notes
[Additional context]
```

Guidelines:
- Highlight main purpose and significant changes
- Use bullet points for clarity
- Avoid repeating PR title/description
- Infer details from available information if needed

Based on:
Title: {PULL_REQUEST_TITLE}
Description: {PULL_REQUEST_DESC}
Patch:
{CODE_DIFF}
"""

MERGE_PR_DESCRIPTION_PROMPT = """
Synthesize multiple PR descriptions into a single, comprehensive summary. Use this markdown format:

```markdown
# Pull Request Summary

## Overview
[One-line summary of overall purpose]

## Changes
- [Change 1]
- [Change 2]

## New Features
- [Feature 1]
- [Feature 2]

##  Refactoring
- [Refactoring 1]
- [Refactoring 2]

## Notes
[Important context from all descriptions]
```

Guidelines:
- Capture essence of all descriptions
- Consolidate similar items
- Focus on most significant aspects
- Eliminate redundancies
- Use Notes for special attention items

PR descriptions to merge:
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
