import pytest
from unittest.mock import patch, Mock
from pull_requests import process_pull_request

# Fixtures
@pytest.fixture
def valid_payload():
    return {
        "pull_request": {
            "comments_url": "https://api.github.com/repos/owner/repo/pulls/1/comments",
            "number": 1,
            "title": "Pull Request Title",
            "body": "Pull Request Description",
        },
        "repository": {
            "full_name": "owner/repo",
        },
        "installation": {
            "id": 123,
        },
    }

@pytest.fixture
def cloud_code_ai_payload(valid_payload):
    valid_payload["repository"]["full_name"] = "Cloud-Code-AI"
    return valid_payload

# Test Cases
def test_process_pull_request_valid_payload(valid_payload):
    with patch("pull_requests.get_installation_access_token") as mock_get_access_token, \
         patch("pull_requests.get_diff_text") as mock_get_diff_text, \
         patch("pull_requests.get_pr_files") as mock_get_pr_files, \
         patch("pull_requests.CodeReviewer") as mock_code_reviewer, \
         patch("pull_requests.create_pr_review_text") as mock_create_review_text, \
         patch("pull_requests.create_review_comments") as mock_create_comments, \
         patch("pull_requests.post_pull_request") as mock_post_review, \
         patch("pull_requests.post_pull_request_comments") as mock_post_comments:

        mock_get_access_token.return_value = "access_token"
        mock_get_diff_text.return_value = "diff_text"
        mock_get_pr_files.return_value = ["file1.py", "file2.py"]
        mock_code_reviewer.return_value.review_pull_request.return_value = Mock(topics={"important": ["topic1", "topic2"]})
        mock_create_review_text.return_value = b"review_text"
        mock_create_comments.return_value = (["comment1", "comment2"], {"important": ["topic1", "topic2"]})

        result, review_desc = process_pull_request(valid_payload)

        assert result is True
        assert review_desc == "review_text"
        mock_post_review.assert_called_once()
        mock_post_comments.assert_has_calls([
            patch.call("https://api.github.com/repos/owner/repo/pulls/1/reviews", "comment1", 123),
            patch.call("https://api.github.com/repos/owner/repo/pulls/1/reviews", "comment2", 123),
        ])

def test_process_pull_request_cloud_code_ai(cloud_code_ai_payload):
    with patch("pull_requests.get_installation_access_token") as mock_get_access_token, \
         patch("pull_requests.get_diff_text") as mock_get_diff_text, \
         patch("pull_requests.get_pr_files") as mock_get_pr_files, \
         patch("pull_requests.CodeReviewer") as mock_code_reviewer, \
         patch("pull_requests.create_pr_review_text") as mock_create_review_text, \
         patch("pull_requests.create_review_comments") as mock_create_comments, \
         patch("pull_requests.post_pull_request") as mock_post_review, \
         patch("pull_requests.post_pull_request_comments") as mock_post_comments, \
         patch("pull_requests.generate_tests") as mock_generate_tests:

        mock_get_access_token.return_value = "access_token"
        mock_get_diff_text.return_value = "diff_text"
        mock_get_pr_files.return_value = ["file1.py", "file2.py"]
        mock_code_reviewer.return_value.review_pull_request.return_value = Mock(topics={"important": ["topic1", "topic2"]})
        mock_create_review_text.return_value = b"review_text"
        mock_create_comments.return_value = (["comment1", "comment2"], {"important": ["topic1", "topic2"]})
        mock_generate_tests.return_value = "generated_tests"

        result, review_desc = process_pull_request(cloud_code_ai_payload)

        assert result is True
        assert review_desc == "review_text"
        mock_post_review.assert_called_once_with("https://api.github.com/repos/Cloud-Code-AI/pulls/1/comments", b"review_text", 123, tests="generated_tests")
        mock_post_comments.assert_has_calls([
            patch.call("https://api.github.com/repos/Cloud-Code-AI/pulls/1/reviews", "comment1", 123),
            patch.call("https://api.github.com/repos/Cloud-Code-AI/pulls/1/reviews", "comment2", 123),
        ])

@pytest.mark.parametrize("payload", [
    {},
    {"pull_request": {}},
    {"repository": {}},
    {"installation": {}},
    {"pull_request": {"comments_url": 123}},
    {"pull_request": {"number": "invalid"}},
    {"repository": {"full_name": 123}},
    {"installation": {"id": "invalid"}},
])
def test_process_pull_request_invalid_payload(payload):
    with pytest.raises(Exception):
        process_pull_request(payload)

# Add more test cases for error handling, boundary conditions, etc.