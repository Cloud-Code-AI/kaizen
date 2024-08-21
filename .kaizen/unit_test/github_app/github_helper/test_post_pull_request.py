import pytest
import requests
from unittest.mock import patch, Mock

# Assuming the function is located in the file /tmp/tmprfhk8pt0/github_app/github_helper/pull_requests.py
from /tmp/tmprfhk8pt0/github_app/github_helper.pull_requests import post_pull_request, get_installation_access_token

# Mock external dependencies
@pytest.fixture
def mock_get_installation_access_token(monkeypatch):
    mock = Mock(return_value="mock_access_token")
    monkeypatch.setattr("pull_requests.get_installation_access_token", mock)
    return mock

@pytest.fixture
def mock_requests_post(monkeypatch):
    mock_response = Mock()
    mock_response.text = "Mock response text"
    mock_post = Mock(return_value=mock_response)
    monkeypatch.setattr("pull_requests.requests.post", mock_post)
    return mock_post

# Test cases
def test_post_pull_request_valid_inputs(mock_get_installation_access_token, mock_requests_post):
    url = "https://api.github.com/repos/owner/repo/pulls"
    data = "Pull request description"
    installation_id = 123

    response = post_pull_request(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, "pull")
    mock_requests_post.assert_called_once_with(
        url,
        headers={
            "Authorization": "Bearer mock_access_token",
            "Accept": "application/vnd.github.v3+json",
        },
        json={"body": f"{data}\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️"},
    )

def test_post_pull_request_empty_data(mock_get_installation_access_token, mock_requests_post):
    url = "https://api.github.com/repos/owner/repo/pulls"
    data = ""
    installation_id = 123

    response = post_pull_request(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, "pull")
    mock_requests_post.assert_called_once_with(
        url,
        headers={
            "Authorization": "Bearer mock_access_token",
            "Accept": "application/vnd.github.v3+json",
        },
        json={"body": "\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️"},
    )

@pytest.mark.parametrize(
    "url",
    [
        "invalid_url",
        None,
    ],
)
def test_post_pull_request_invalid_url(url, mock_get_installation_access_token, mock_requests_post):
    data = "Pull request description"
    installation_id = 123

    with pytest.raises(Exception):
        post_pull_request(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, "pull")
    mock_requests_post.assert_not_called()

def test_post_pull_request_token_retrieval_error(mock_get_installation_access_token, mock_requests_post):
    url = "https://api.github.com/repos/owner/repo/pulls"
    data = "Pull request description"
    installation_id = 123

    mock_get_installation_access_token.side_effect = Exception("Token retrieval error")

    with pytest.raises(Exception):
        post_pull_request(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, "pull")
    mock_requests_post.assert_not_called()

def test_post_pull_request_request_error(mock_get_installation_access_token, mock_requests_post):
    url = "https://api.github.com/repos/owner/repo/pulls"
    data = "Pull request description"
    installation_id = 123

    mock_requests_post.side_effect = requests.exceptions.RequestException("Request error")

    with pytest.raises(requests.exceptions.RequestException):
        post_pull_request(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, "pull")
    mock_requests_post.assert_called_once_with(
        url,
        headers={
            "Authorization": "Bearer mock_access_token",
            "Accept": "application/vnd.github.v3+json",
        },
        json={"body": f"{data}\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️"},
    )