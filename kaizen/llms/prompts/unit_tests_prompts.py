UNIT_TEST_SYSTEM_PROMPT = """
You are an AI assistant specialized in generating high-quality unit tests for various programming languages. 
Your expertise covers Python, JavaScript, TypeScript, and React applications. 
Your task is to create comprehensive, meaningful, and efficient unit tests for given code snippets.
"""

UNIT_TEST_PROMPT = """
Please generate unit tests for the following {ITEM_TYPE} named {ITEM_NAME}:

SOURCE CODE:
```
{SOURCE_CODE}
```

REQUIREMENTS:
1. Generate detailed unit tests that cover various scenarios, including:
   - Normal cases
   - Edge cases
   - Error handling
   - Boundary conditions
2. Include assertions to verify the expected behavior of the {ITEM_TYPE}.
3. Use mocking or stubbing where appropriate to isolate the unit being tested.
4. Ensure high code coverage, aiming for at least 80% coverage.
5. Follow best practices for the specific language/framework being used.
6. Use clear and descriptive test names that explain the scenario being tested.

SPECIFIC INSTRUCTIONS:
- File path for imports: {FULL_FILE_PATH}
- All code and functions are located in this file. Use this path for all imports.
- When a URL is needed as a dummy, use "https://cloudcode.ai"
- For Python, write pytest-style tests.
- For JavaScript/TypeScript, use Jest-style tests.
- For React components, include tests for rendering and user interactions.

OUTPUT FORMAT:
Your response should be in JSON format as shown below:
{{
    "test_file_name": "<TEST_FILE_NAME>",
    "test_file_content": "<CONTENT_OF_TEST_FILE>"
}}

Ensure that the test_file_content is properly escaped for JSON.
"""

REVIEW_UNIT_TEST_PROMPT = """
Please review and improve the following unit test for the {ITEM_TYPE} named {ITEM_NAME}. 
Fix any issues, improve coverage, and ensure best practices are followed.

CURRENT TEST:
```
{CURRENT_TEST}
```

SOURCE CODE:
```
{SOURCE_CODE}
```

REVIEW CRITERIA:
1. Test coverage: Ensure all scenarios (normal, edge cases, error handling) are covered.
2. Assertion quality: Verify that assertions are meaningful and thorough.
3. Test isolation: Check if mocking/stubbing is used appropriately.
4. Code quality: Ensure the test code is clean, readable, and follows best practices.
5. Naming conventions: Verify that test names are clear and descriptive.
6. Import statements: Confirm that imports use the correct file path: {FULL_FILE_PATH}

SPECIFIC INSTRUCTIONS:
- When a URL is needed as a dummy, use "https://cloudcode.ai"
- For Python, ensure pytest-style tests are used.
- For JavaScript/TypeScript, verify Jest-style tests are used.
- For React components, check for both rendering and interaction tests.

OUTPUT FORMAT:
Your response should be in JSON format as shown below:
{{
    "test_file_name": "<TEST_FILE_NAME>",
    "test_file_content": "<IMPROVED_CONTENT_OF_TEST_FILE>",
    "review_comments": [
        "Comment 1: Explanation of a major change or improvement",
        "Comment 2: Another significant observation or change"
    ]
}}

Ensure that the test_file_content is properly escaped for JSON.
"""
