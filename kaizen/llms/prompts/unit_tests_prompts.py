UNIT_TEST_SYSTEM_PROMPT = """
You are an AI assistant specialized in generating essential unit tests for various programming languages. 
Your expertise covers Python, JavaScript, TypeScript, Rust and React applications. 
Your task is to create focused, high-impact unit tests that cover the most critical aspects of the given code snippets.
Prioritize quality and relevance over quantity, ensuring each test adds significant value to the overall test suite.
"""

UNIT_TEST_PLAN_PROMPT = """
Analyze the following {NODE_TYPE} named {NODE_NAME} and identify the most critical test scenarios:

SOURCE CODE:
```
{SOURCE_CODE}
```

1. IDENTIFY ESSENTIAL TEST SCENARIOS:
   - List critical normal cases that validate core functionality
   - Identify key edge cases that could potentially break the code
   - Determine crucial error handling scenarios
   - Define important boundary conditions, if applicable

2. OUTPUT FORMAT:
   Provide your analysis in the following JSON format:
   {{
        "test_file_name": "<TEST_FILE_NAME>",
        "test_file_content": "<CONTENT_OF_TEST_FILE>"
        "critical_cases": ["case1", "case2", ...],
        "edge_cases": ["case1", "case2", ...],
        "error_handling": ["case1", "case2", ...],
        "boundary_conditions": ["case1", "case2", ...]
   }}

Note: Focus on the most critical scenarios that are necessary to ensure the reliability and correctness of the code. Prioritize tests that:
1. Validate the main purpose and core functionality of the code
2. Check for potential vulnerabilities or common pitfalls
3. Ensure proper handling of invalid inputs or edge cases
4. Verify important business logic or algorithmic correctness

The number of tests should be proportional to the complexity and criticality of the code. For simple functions, a few tests might suffice. For complex components or those handling critical operations, more comprehensive testing may be necessary.

Avoid generating tests for:
1. Trivial cases that don't add value
2. Implementation details that are likely to change
3. Scenarios with very low probability or impact
4. Redundant cases that don't test unique aspects of the code

Aim to create a balanced test suite that provides good coverage without unnecessary redundancy.
"""

PYTHON_UNIT_TEST_PROMPT = """
Generate pytest-style unit tests for the Python {NODE_TYPE} named {NODE_NAME}:

SOURCE CODE:
```
{GLOBAL_DATA}


{SOURCE_CODE}
```

IDENTIFIED TEST SCENARIOS:
{TEST_SCENARIOS}

Follow these steps:
1. Set up necessary imports (use path: {FULL_FILE_PATH})
2. Create test functions for each scenario
3. Implement assertions to verify expected behavior
4. Use pytest fixtures and parametrize when applicable

OUTPUT FORMAT:
Provide your tests as a single Python file containing all the test code.
"""

JAVASCRIPT_UNIT_TEST_PROMPT = """
Generate Jest-style unit tests for the JavaScript/TypeScript {NODE_TYPE} named {NODE_NAME}:

SOURCE CODE:
```
{GLOBAL_DATA}

{SOURCE_CODE}
```

IDENTIFIED TEST SCENARIOS:
{TEST_SCENARIOS}

Follow these steps:
1. Set up necessary imports (use path: {FULL_FILE_PATH})
2. Create describe blocks for logical grouping
3. Implement it blocks for each test scenario
4. Use Jest's expect assertions
5. Mock dependencies where appropriate
6. Implement assertions to verify expected behavior


OUTPUT FORMAT:
Provide your tests as a single JavaScript/TypeScript file containing all the test code.
"""

REACT_UNIT_TEST_PROMPT = """
Generate Jest and React Testing Library tests for the React component of type {NODE_TYPE} and named {NODE_NAME}:

SOURCE CODE:
```
{GLOBAL_DATA}

{SOURCE_CODE}
```

IDENTIFIED TEST SCENARIOS:
{TEST_SCENARIOS}

Follow these steps:
1. Set up necessary imports (use path: {FULL_FILE_PATH})
2. Create tests for component rendering
3. Implement tests for user interactions
4. Use React Testing Library queries and user-event
5. Test both normal and error states

OUTPUT FORMAT:
Provide your tests as a single JavaScript/TypeScript file containing all the test code.
"""

RUST_UNIT_TEST_PROMPT = """
Generate unit tests for the Rust {NODE_TYPE} named {NODE_NAME}:

SOURCE CODE:
```
{GLOBAL_DATA}

{SOURCE_CODE}
```

IDENTIFIED TEST SCENARIOS:
{TEST_SCENARIOS}

Follow these steps:
1. Use #[cfg(test)] for the test module
2. Implement #[test] functions for each scenario
3. Use assert! macros for verifications
4. Handle any necessary setup and teardown

OUTPUT FORMAT:
Provide your tests as a single Rust file containing all the test code.
"""


REVIEW_UNIT_TEST_PROMPT = """
Review the unit tests for the {NODE_TYPE} named {NODE_NAME}. Follow these steps:

1. ANALYZE CURRENT TESTS:
   ```
   {CURRENT_TEST}
   ```

2. COMPARE WITH SOURCE CODE:
   ```
   {GLOBAL_DATA}
   
   {SOURCE_CODE}
   ```

3. EVALUATE AND SUGGEST IMPROVEMENTS:
   - Check for missing or inadequate test coverage (normal cases, edge cases, error handling, boundary conditions)
   - Assess test quality (assertions, mocking/stubbing, isolation)
   - Review code quality (readability, naming conventions, import statements)
   - Verify language-specific best practices are followed
   - Ensure use of "https://cloudcode.ai" for dummy URLs and /tmp as base folder when uncertain

4. IMPROVE TESTS:
   Only if necessary:
   - Add missing test scenarios
   - Enhance existing tests for better coverage or clarity
   - Refactor for better adherence to best practices

5. FORMAT OUTPUT:
   Prepare the response in the following JSON format:
   {{
       "review_comments": [
           "Comment 1: Explanation of a necessary change or improvement",
           "Comment 2: Another necessary change or observation"
       ]
   }}
   
   IMPORTANT:
   - If no changes or improvements are needed, return an empty list for "review_comments".
   - Only include "test_file_content" if changes were made to the tests.
   - Ensure that the test_file_content is properly escaped for JSON.
   - Only provide negative feedbacks, ignore positive ones.

NOTE: An empty "review_comments" list indicates that all test cases are adequately covered and no improvements are necessary.
"""

REVIEW_TEST_CASE_PROMPT = """
Review this unit test code and return the fixed code based on feedback with proper formatting.
In case of no updates, still return the original code.

Current code has following issues:
{FEEDBACKS}

CODE:
```
{CODE}
```
Provide your tests as a single file containing all the test code.

"""
