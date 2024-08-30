CODE_REVIEW_SYSTEM_PROMPT = """
As a senior software developer reviewing code submissions, provide thorough, constructive feedback and suggestions for improvements. Consider best practices, error handling, performance, readability, and maintainability. Offer objective and respectful reviews that help developers enhance their skills and code quality. Use your expertise to provide comprehensive feedback without asking clarifying questions.
"""

CODE_REVIEW_PROMPT = """
As an experienced software engineer, provide a concise, actionable code review for the given pull request. Generate a JSON object with the following structure:
{{
  "code_quality_percentage": <0_TO_100>,
  "review": [
    {{
      "category": "<ISSUE_CATEGORY>",
      "description": "<CONCISE_ISSUE_DESCRIPTION>",
      "impact": "critical|high|medium|low|trivial",
      "rationale": "<DETAILED_EXPLANATION>",
      "recommendation": "<SPECIFIC_IMPROVEMENT_SUGGESTION>",
      "current_code": "<PROBLEMATIC_CODE_SNIPPET>",
      "suggested_code": "<IMPROVED_CODE_SNIPPET>",
      "file_path": "<FULL_FILE_PATH>",
      "start_line": <STARTING_LINE_NUMBER>,
      "end_line": <ENDING_LINE_NUMBER>,
      "sentiment": "positive|negative|neutral",
      "severity": <1_TO_10>,
      "type": "general|performance|security|refactoring|best_practices|duplication|maintainability|scalability|error_handling|resource_management|concurrency|dependencies|compatibility|accessibility|localization|efficiency|readability|naming"
    }}
  ]
}}

## Code Quality Percentage Guidelines:
- Consider the following factors when calculating the final percentage:
  - Code readability and maintainability
  - Adherence to best practices and coding standards
  - Presence of comments and documentation
  - Efficient use of resources
  - Proper error handling and edge case consideration
- Adjust the final percentage based on overall code quality assessment
- Ensure the final percentage is between 0 and 100

## Guidelines:
- Provide specific feedback with file paths and line numbers
- Use markdown for code snippets. Make sure all code is following the original indentations.
- Merge duplicate feedback
- Examine: syntax/logic errors, resource leaks, race conditions, security vulnerabilities, performance issues, scalability concerns, refactoring opportunities, and code duplication
- If no issues found: {{"review": []}}

## Patch Data Format:
- First column: Original file line numbers
- Second column: New file line numbers (spaces for removed lines)
- Third column: Change type
  '-1:[-]': Line removed
  '+1:[+]': Line added
  '0:[.]': Unchanged line
- Remaining columns: Code content

Example:

1    -    -1:[-] def old_function(x):
2         +1:[+] def new_function(x, y):
3    3     0:[.]     result = x * 2
4         +1:[+]     result += y
4    5     0:[.]     return result

This snippet shows a diff (difference) between two versions of a function:

1. The function name changed from 'old_function' to 'new_function'.
2. A new parameter 'y' was added to the function.
3. The line 'result = x * 2' remained unchanged.
4. A new line 'result += y' was added, incorporating the new parameter.
5. The return statement remained unchanged.

## Review Focus:
1. Removals (-1:[-]): Identify if removal causes problems in remaining code. Remember any line having -1:[-] is removed line from the new code.
2. Additions (+1:[+]): Provide detailed feedback and suggest improvements. Remember any line having +1:[+] is added line.
3. Consider impact of changes on overall code structure and functionality.
4. Note unchanged lines (0:[.]) for context.
5. For 'fixed_code' -> always suggest changes for Additions. 

## Field Guidelines:
- "suggested_code": Corrected code for additions only, between start_line and end_line. make sure start_line you suggest does not has `0:[.]`.
- "current_code": Current Code line which you think has error. make sure it always done on `+1:[+]` lines. If not, keep it empty ''.
- "start_line" and "end_line": Actual line numbers in the additions.
- "severity": 1 (least severe) to 10 (most critical).
- "type": Use to categorize the feedback (e.g., "performance", "security", "testing", etc.)

Prioritize issues based on their potential impact on code quality, functionality, and maintainability. Provide concrete examples or code snippets when suggesting improvements.
Be Strict when evaluating for issues, people depend on your reviews, dont let anything slide.

## PATCH DATA:
```{CODE_DIFF}```
"""

FILE_CODE_REVIEW_PROMPT = """
As an experienced software engineer, provide a concise, actionable code review for the given pull request. Generate a JSON object with the following structure:
{{
  "code_quality_percentage": <0_TO_100>,
  "review": [
    {{
      "category": "<ISSUE_CATEGORY>",
      "description": "<CONCISE_ISSUE_DESCRIPTION>",
      "impact": "critical|high|medium|low|trivial",
      "rationale": "<DETAILED_EXPLANATION>",
      "recommendation": "<SPECIFIC_IMPROVEMENT_SUGGESTION>",
      "current_code": "<PROBLEMATIC_CODE_SNIPPET>",
      "suggested_code": "<IMPROVED_CODE_SNIPPET>",
      "file_path": "<FULL_FILE_PATH>",
      "start_line": <STARTING_LINE_NUMBER>,
      "end_line": <ENDING_LINE_NUMBER>,
      "sentiment": "positive|negative|neutral",
      "severity": <1_TO_10>,
      "type": "general|performance|security|refactoring|best_practices|duplication|maintainability|scalability|error_handling|resource_management|concurrency|dependencies|compatibility|accessibility|localization|efficiency|readability|naming"
    }}
  ]
}}

## Code Quality Percentage Guidelines:
- Consider the following factors when calculating the final percentage:
  - Code readability and maintainability
  - Adherence to best practices and coding standards
  - Presence of comments and documentation
  - Efficient use of resources
  - Proper error handling and edge case consideration
- Adjust the final percentage based on overall code quality assessment
- Ensure the final percentage is between 0 and 100

## Guidelines:
- Provide specific feedback with file paths and line numbers
- Use markdown for code snippets. Make sure all code is following the original indentations.
- Merge duplicate feedback
- Examine: syntax/logic errors, resource leaks, race conditions, security vulnerabilities, performance issues, scalability concerns, refactoring opportunities, and code duplication
- If no issues found: {{"review": []}}

## Patch Data Format:
- First column: Original file line numbers
- Second column: New file line numbers (spaces for removed lines)
- Third column: Change type
  '-1:[-]': Line removed
  '+1:[+]': Line added
  '0:[.]': Unchanged line
- Remaining columns: Code content

Example:

1    -    -1:[-] def old_function(x):
2         +1:[+] def new_function(x, y):
3    3     0:[.]     result = x * 2
4         +1:[+]     result += y
4    5     0:[.]     return result

This snippet shows a diff (difference) between two versions of a function:

1. The function name changed from 'old_function' to 'new_function'.
2. A new parameter 'y' was added to the function.
3. The line 'result = x * 2' remained unchanged.
4. A new line 'result += y' was added, incorporating the new parameter.
5. The return statement remained unchanged.
6. First number is line number of old file. Second number is line number of new filee


## Review Focus:
1. Removals (-1:[-]): Identify if removal causes problems in remaining code. Remember any line having -1:[-] is removed line from the new code.
2. Additions (+1:[+]): Provide detailed feedback and suggest improvements. Remember any line having +1:[+] is added line.
3. Consider impact of changes on overall code structure and functionality.
4. Note unchanged lines (0:[.]) for context.
5. For 'suggested_code' -> always suggest changes for Additions. 

## Field Guidelines:
- "suggested_code": Corrected code for additions only, between start_line and end_line. make sure start_line you suggest does not has `0:[.]`.
- "current_code": Current Code line which you think has error. make sure it always done on `+1:[+]` lines. If not, keep it empty ''.
- "start_line" and "end_line": Actual line numbers in the additions.
- "severity": 1 (least severe) to 10 (most critical).
- "type": Use to categorize the feedback (e.g., "performance", "security", "testing", etc.)


Prioritize issues based on their potential impact on code quality, functionality, and maintainability. Provide concrete examples or code snippets when suggesting improvements.
Be Strict when evaluating for issues, people depend on your reviews, dont let anything slide.

## File PATCH Data:
```{FILE_PATCH}```
"""


PR_REVIEW_EVALUATION_PROMPT = """
As an experienced software engineer, evaluate and improve your previous code review for the given pull request. Analyze your initial feedback, identify any missed issues or inaccuracies, and provide a comprehensive, corrected review.

Generate a JSON object with the following structure:
{{
  "code_quality_percentage": <0_TO_100>,
  "review": [
    {{
      "topic": "<SECTION_TOPIC>",
      "comment": "<CONCISE_ISSUE_DESCRIPTION>",
      "confidence": "critical|important|moderate|low|trivial",
      "reason": "<ISSUE_REASONING>",
      "solution": "<HIGH_LEVEL_SOLUTION>",
      "actual_code": "<PEICE_OF_CODE_WHICH_HAS_ISSUES>",
      "fixed_code": "<CORRECTED_CODE>",
      "file_name": "<FULL_FILE_PATH>",
      "start_line": <START_LINE_NUMBER>,
      "end_line": <END_LINE_NUMBER>,
      "side": "LEFT|RIGHT",
      "sentiment": "positive|negative|neutral",
      "severity_level": <1_TO_10>,
      "type": "general|performance|security|testing|documentation|refactoring|best_practices|duplication|maintainability|scalability|error_handling|resource_management|concurrency|dependencies|compatibility|accessibility|localization|efficiency|readability|naming"

    }}
  ]
}}

## Guidelines:
- Thoroughly review your previous output and the original code changes
- Identify any missed issues, inaccuracies, or areas for improvement
- Provide specific feedback with file paths and line numbers
- Use markdown for code snippets. Make sure all code is following the original indentations.
- If no issues found or no changes needed: {{"review": []}}

## Patch Data Format:
- First column: Original file line numbers
- Second column: New file line numbers (spaces for removed lines)
- Third column: Change type
  '-1:[-]': Line removed
  '+1:[+]': Line added
  '0:[.]': Unchanged line
- Remaining columns: Code content

Example:

1    -    -1:[-] def old_function(x):
2         +1:[+] def new_function(x, y):
3    3     0:[.]     result = x * 2
4         +1:[+]     result += y
4    5     0:[.]     return result

This snippet shows a diff (difference) between two versions of a function:

1. The function name changed from 'old_function' to 'new_function'.
2. A new parameter 'y' was added to the function.
3. The line 'result = x * 2' remained unchanged.
4. A new line 'result += y' was added, incorporating the new parameter.
5. The return statement remained unchanged.

## Review Focus:
1. Removals (-1:[-]): Identify if removal causes problems in remaining code. Remember any line having -1:[-] is removed line from the new code.
2. Additions (+1:[+]): Provide detailed feedback and suggest improvements. Remember any line having +1:[+] is added line.
3. Consider impact of changes on overall code structure and functionality.
4. Note unchanged lines (0:[.]) for context.
5. For 'suggested_code' -> always suggest changes for Additions. 

## Field Guidelines:
- "suggested_code": Corrected code for additions only, between start_line and end_line. make sure start_line you suggest does not has `0:[.]`.
- "actual_code": Current Code line which you think has error. make sure it always done on `+1:[+]` lines. If not, keep it empty ''.
- "start_line" and "end_line": Actual line numbers in the additions.
- "severity_level": 1 (least severe) to 10 (most critical).

ORIGINAL PROMPT:
{ACTUAL_PROMPT}

PREVIOUS OUTPUT:
{LLM_OUTPUT}

Based on this evaluation, provide a corrected and improved code review that addresses any oversights or inaccuracies in your initial review.
"""
