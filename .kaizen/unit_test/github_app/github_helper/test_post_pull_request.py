import pytest
import requests
from unittest.mock import patch, MagicMock
from github_app.github_helper.pull_requests import post_pull_request, get_installation_access_token, PULL_REQUEST_PERMISSION

@pytest.fixture
def mock_access_token():
    return "mocked_access_token"

@pytest.fixture
def mock_get_installation_access_token(mock_access_token):
    with patch('github_app.github_helper.pull_requests.get_installation_access_token') as mock:
        mock.return_value = mock_access_token
        yield mock

@pytest.fixture
def mock_requests_post():
    with patch('github_app.github_helper.pull_requests.requests.post') as mock:
        yield mock

def test_successful_post_pull_request(mock_get_installation_access_token, mock_requests_post, mock_access_token):
    url = "https://api.github.com/repos/owner/repo/issues/1/comments"
    data = "Test comment"
    installation_id = 12345

    mock_response = MagicMock()
    mock_response.text = '{"id": 1, "body": "Test comment"}'
    mock_requests_post.return_value = mock_response

    post_pull_request(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, PULL_REQUEST_PERMISSION)
    mock_requests_post.assert_called_once_with(
        url,
        headers={
            "Authorization": f"Bearer {mock_access_token}",
            "Accept": "application/vnd.github.v3+json",
        },
        json={
            "body": f"{data}\n\n> ✨ Generated with love by [Kaizen](https://cloudcode.ai) ❤️"
        }
    )

def test_kaizen_signature_added(mock_get_installation_access_token, mock_requests_post):
    url = "https://api.github.com/repos/owner/repo/issues/1/comments"
    data = "Test comment"
    installation_id = 12345

    post_pull_request(url, data, installation_id)

    called_args = mock_requests_post.call_args[1]
    assert "Generated with love by [Kaizen](https://cloudcode.ai)" in called_args['json']['body']

@pytest.mark.parametrize("data", [
    "",
    "A" * 65536,  # GitHub's maximum comment length
    "Unicode: こんにちは世界",
])
def test_various_comment_data(mock_get_installation_access_token, mock_requests_post, data):
    url = "https://api.github.com/repos/owner/repo/issues/1/comments"
    installation_id = 12345

    post_pull_request(url, data, installation_id)

    called_args = mock_requests_post.call_args[1]
    assert data in called_args['json']['body']

def test_invalid_installation_id(mock_get_installation_access_token):
    url = "https://api.github.com/repos/owner/repo/issues/1/comments"
    data = "Test comment"
    installation_id = -1

    mock_get_installation_access_token.side_effect = ValueError("Invalid installation ID")

    with pytest.raises(ValueError):
        post_pull_request(url, data, installation_id)

def test_network_error(mock_get_installation_access_token, mock_requests_post):
    url = "https://api.github.com/repos/owner/repo/issues/1/comments"
    data = "Test comment"
    installation_id = 12345

    mock_requests_post.side_effect = requests.ConnectionError("Network error")

    with pytest.raises(requests.ConnectionError):
        post_pull_request(url, data, installation_id)

def test_github_api_error(mock_get_installation_access_token, mock_requests_post):
    url = "https://api.github.com/repos/owner/repo/issues/1/comments"
    data = "Test comment"
    installation_id = 12345

    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("API error")
    mock_requests_post.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        post_pull_request(url, data, installation_id)

def test_invalid_access_token(mock_get_installation_access_token, mock_requests_post):
    url = "https://api.github.com/repos/owner/repo/issues/1/comments"
    data = "Test comment"
    installation_id = 12345

    mock_get_installation_access_token.return_value = "invalid_token"
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_requests_post.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        post_pull_request(url, data, installation_id)

def test_rate_limiting_error(mock_get_installation_access_token, mock_requests_post):
    url = "https://api.github.com/repos/owner/repo/issues/1/comments"
    data = "Test comment"
    installation_id = 12345

    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_requests_post.return_value = mock_response

    with pytest.raises(requests.HTTPError):
        post_pull_request(url, data, installation_id)

@pytest.mark.parametrize("installation_id", [1, 2**31 - 1])  # Minimum and maximum 32-bit integer
def test_boundary_installation_id(mock_get_installation_access_token, mock_requests_post, installation_id):
    url = "https://api.github.com/repos/owner/repo/issues/1/comments"
    data = "Test comment"

    post_pull_request(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, PULL_REQUEST_PERMISSION)

def test_maximum_comment_length(mock_get_installation_access_token, mock_requests_post):
    url = "https://api.github.com/repos/owner/repo/issues/1/comments"
    data = "A" * 65536  # GitHub's maximum comment length
    installation_id = 12345

    post_pull_request(url, data, installation_id)

    called_args = mock_requests_post.call_args[1]
    assert len(called_args['json']['body']) <= 65536

def test_minimum_required_permissions(mock_get_installation_access_token, mock_requests_post):
    url = "https://api.github.com/repos/owner/repo/issues/1/comments"
    data = "Test comment"
    installation_id = 12345

    post_pull_request(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, PULL_REQUEST_PERMISSION)