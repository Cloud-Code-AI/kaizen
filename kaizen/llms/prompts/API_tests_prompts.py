API_TEST_SYSTEM_PROMPT = """
You are an advanced AI assistant specializing in writing API tests using Pytest. 
Your task is to write clear, efficient and meaningful API tests only for the given API endpoint. """

API_METHOD_PROMPT = """
Analyze the HTTP {method} method for endpoint {path} with the following schema:
{method_code}
BASE-URL: {base_url}
Generate comprehensive pytest-style API tests for this endpoint. Include the following:
1. Identify key test cases for the method schema.
2. Test for both valid and invalid request formats.
3. Provide detailed assert messages for both successful and error responses.
4. Identify key edge cases (boundary values, unusual inputs) that shall potentially fail.
5. If applicable write authentication test cases but use pytest decorator: @pytest.mark.skip stating reason as Authentication tests disabled.
Use pytest best practices and decorators. 
Provide your tests as a well structured Python file containing all the test code.
"""
