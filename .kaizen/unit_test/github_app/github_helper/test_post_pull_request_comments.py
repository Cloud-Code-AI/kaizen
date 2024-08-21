import pytest
import requests
from unittest.mock import patch, Mock

# Assuming the function is located in the following path
from /tmp/tmpn_ihnj4m/github_app/github_helper.pull_requests import post_pull_request_comments

# Mocking the get_installation_access_token function
def mock_get_installation_access_token(installation_id, permission):
    return "mock_access_token"

# Mocking the logger
class MockLogger:
    def debug(self, msg):
        pass

logger = MockLogger()

@pytest.fixture
def valid_review():
    return {
        "file_name": "test_file.py",
        "start_line": 1,
        "end_line": 5,
        "comment": "This is a test comment."
    }

@pytest.fixture
def headers():
    return {
        "Authorization": "Bearer mock_access_token",
        "Accept": "application/vnd.github.v3+json",
    }

@pytest.fixture
def mock_post():
    with patch('requests.post') as mock_post:
        yield mock_post

@pytest.fixture
def mock_token():
    with patch('/tmp/tmpn_ihnj4m/github_app/github_helper.pull_requests.get_installation_access_token', mock_get_installation_access_token):
        yield

@pytest.fixture
def mock_logger():
    with patch('/tmp/tmpn_ihnj4m/github_app/github_helper.pull_requests.logger', logger):
        yield

def test_post_pull_request_comments_valid_input(valid_review, headers, mock_post, mock_token, mock_logger):
    url = "https://api.github.com/repos/test/repo/pulls/1/reviews"
    response_mock = Mock()
    response_mock.text = "Success"
    mock_post.return_value = response_mock

    post_pull_request_comments(url, valid_review, 12345)

    mock_post.assert_called_once_with(url, headers=headers, json={
        "event": "REQUEST_CHANGES",
        "comments": [
            {
                "path": "test_file.py",
                "start_line": 1,
                "line": 5,
                "body": "This is a test comment.",
            }
        ],
    })

@pytest.mark.parametrize("review", [
    {"file_name": "test_file.py", "start_line": 1, "end_line": 1, "comment": "Single line comment"},
    {"file_name": "test_file.py", "start_line": 0, "end_line": 5, "comment": "Start line is zero"},
    {"file_name": "test_file.py", "start_line": 1, "end_line": 10000, "comment": "End line is very large"}
])
def test_post_pull_request_comments_boundary_conditions(review, headers, mock_post, mock_token, mock_logger):
    url = "https://api.github.com/repos/test/repo/pulls/1/reviews"
    response_mock = Mock()
    response_mock.text = "Success"
    mock_post.return_value = response_mock

    post_pull_request_comments(url, review, 12345)

    mock_post.assert_called_once_with(url, headers=headers, json={
        "event": "REQUEST_CHANGES",
        "comments": [
            {
                "path": review["file_name"],
                "start_line": review["start_line"],
                "line": review["end_line"],
                "body": review["comment"],
            }
        ],
    })

def test_post_pull_request_comments_empty_review(headers, mock_post, mock_token, mock_logger):
    url = "https://api.github.com/repos/test/repo/pulls/1/reviews"
    review = {"file_name": "test_file.py", "start_line": 1, "end_line": 5, "comment": ""}
    response_mock = Mock()
    response_mock.text = "Success"
    mock_post.return_value = response_mock

    post_pull_request_comments(url, review, 12345)

    mock_post.assert_called_once_with(url, headers=headers, json={
        "event": "REQUEST_CHANGES",
        "comments": [
            {
                "path": "test_file.py",
                "start_line": 1,
                "line": 5,
                "body": "",
            }
        ],
    })

def test_post_pull_request_comments_special_characters(headers, mock_post, mock_token, mock_logger):
    url = "https://api.github.com/repos/test/repo/pulls/1/reviews"
    review = {"file_name": "test_file.py", "start_line": 1, "end_line": 5, "comment": "Special characters: !@#$%^&*()"}
    response_mock = Mock()
    response_mock.text = "Success"
    mock_post.return_value = response_mock

    post_pull_request_comments(url, review, 12345)

    mock_post.assert_called_once_with(url, headers=headers, json={
        "event": "REQUEST_CHANGES",
        "comments": [
            {
                "path": "test_file.py",
                "start_line": 1,
                "line": 5,
                "body": "Special characters: !@#$%^&*()",
            }
        ],
    })

def test_post_pull_request_comments_invalid_url(valid_review, headers, mock_post, mock_token, mock_logger):
    url = "invalid_url"
    response_mock = Mock()
    response_mock.text = "Failed"
    mock_post.return_value = response_mock

    with pytest.raises(requests.exceptions.RequestException):
        post_pull_request_comments(url, valid_review, 12345)

def test_post_pull_request_comments_non_existent_installation_id(valid_review, headers, mock_post, mock_logger):
    url = "https://api.github.com/repos/test/repo/pulls/1/reviews"
    with patch('/tmp/tmpn_ihnj4m/github_app/github_helper.pull_requests.get_installation_access_token', side_effect=Exception("Installation ID not found")):
        with pytest.raises(Exception, match="Installation ID not found"):
            post_pull_request_comments(url, valid_review, 99999)

def test_post_pull_request_comments_invalid_access_token(valid_review, headers, mock_post, mock_logger):
    url = "https://api.github.com/repos/test/repo/pulls/1/reviews"
    with patch('/tmp/tmpn_ihnj4m/github_app/github_helper.pull_requests.get_installation_access_token', return_value="invalid_token"):
        response_mock = Mock()
        response_mock.text = "Unauthorized"
        response_mock.status_code = 401
        mock_post.return_value = response_mock

        post_pull_request_comments(url, valid_review, 12345)

        mock_post.assert_called_once_with(url, headers={
            "Authorization": "Bearer invalid_token",
            "Accept": "application/vnd.github.v3+json",
        }, json={
            "event": "REQUEST_CHANGES",
            "comments": [
                {
                    "path": "test_file.py",
                    "start_line": 1,
                    "line": 5,
                    "body": "This is a test comment.",
                }
            ],
        })

def test_post_pull_request_comments_failed_api_request(valid_review, headers, mock_post, mock_token, mock_logger):
    url = "https://api.github.com/repos/test/repo/pulls/1/reviews"
    response_mock = Mock()
    response_mock.text = "Server Error"
    response_mock.status_code = 500
    mock_post.return_value = response_mock

    post_pull_request_comments(url, valid_review, 12345)

    mock_post.assert_called_once_with(url, headers=headers, json={
        "event": "REQUEST_CHANGES",
        "comments": [
            {
                "path": "test_file.py",
                "start_line": 1,
                "line": 5,
                "body": "This is a test comment.",
            }
        ],
    })