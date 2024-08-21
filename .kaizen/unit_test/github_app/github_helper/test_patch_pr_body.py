import pytest
from unittest.mock import patch, Mock
import requests
from /tmp/tmprfhk8pt0/github_app/github_helper.pull_requests import patch_pr_body

# Mocking the external dependencies
@pytest.fixture
def mock_get_installation_access_token():
    with patch('/tmp/tmprfhk8pt0/github_app/github_helper.pull_requests.get_installation_access_token') as mock:
        yield mock

@pytest.fixture
def mock_requests_patch():
    with patch('requests.patch') as mock:
        yield mock

@pytest.fixture
def mock_logger():
    with patch('/tmp/tmprfhk8pt0/github_app/github_helper.pull_requests.logger') as mock:
        yield mock

def test_successful_patch_pr_body(mock_get_installation_access_token, mock_requests_patch, mock_logger):
    mock_get_installation_access_token.return_value = 'fake_access_token'
    mock_response = Mock()
    mock_response.text = 'Success'
    mock_requests_patch.return_value = mock_response

    url = 'https://api.github.com/repos/user/repo/pulls/1'
    data = 'Updated PR body'
    installation_id = 123

    patch_pr_body(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            'Authorization': 'Bearer fake_access_token',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={'body': data}
    )
    mock_logger.debug.assert_called_once_with('Patch Pull request response: Success')

@pytest.mark.parametrize("data", ["", "a" * 65536, "Unicode characters: 你好"])
def test_patch_pr_body_edge_cases(data, mock_get_installation_access_token, mock_requests_patch, mock_logger):
    mock_get_installation_access_token.return_value = 'fake_access_token'
    mock_response = Mock()
    mock_response.text = 'Success'
    mock_requests_patch.return_value = mock_response

    url = 'https://api.github.com/repos/user/repo/pulls/1'
    installation_id = 123

    patch_pr_body(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            'Authorization': 'Bearer fake_access_token',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={'body': data}
    )
    mock_logger.debug.assert_called_once_with('Patch Pull request response: Success')

def test_invalid_installation_id(mock_get_installation_access_token, mock_requests_patch, mock_logger):
    mock_get_installation_access_token.side_effect = ValueError("Invalid installation_id")

    url = 'https://api.github.com/repos/user/repo/pulls/1'
    data = 'Updated PR body'
    installation_id = -1

    with pytest.raises(ValueError, match="Invalid installation_id"):
        patch_pr_body(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_requests_patch.assert_not_called()
    mock_logger.debug.assert_not_called()

def test_failed_to_retrieve_access_token(mock_get_installation_access_token, mock_requests_patch, mock_logger):
    mock_get_installation_access_token.side_effect = Exception("Failed to retrieve access token")

    url = 'https://api.github.com/repos/user/repo/pulls/1'
    data = 'Updated PR body'
    installation_id = 123

    with pytest.raises(Exception, match="Failed to retrieve access token"):
        patch_pr_body(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_requests_patch.assert_not_called()
    mock_logger.debug.assert_not_called()

def test_http_error_response(mock_get_installation_access_token, mock_requests_patch, mock_logger):
    mock_get_installation_access_token.return_value = 'fake_access_token'
    mock_response = Mock()
    mock_response.text = 'Error'
    mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP Error")
    mock_requests_patch.return_value = mock_response

    url = 'https://api.github.com/repos/user/repo/pulls/1'
    data = 'Updated PR body'
    installation_id = 123

    with pytest.raises(requests.HTTPError, match="HTTP Error"):
        patch_pr_body(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            'Authorization': 'Bearer fake_access_token',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={'body': data}
    )
    mock_logger.debug.assert_called_once_with('Patch Pull request response: Error')

def test_network_connection_error(mock_get_installation_access_token, mock_requests_patch, mock_logger):
    mock_get_installation_access_token.return_value = 'fake_access_token'
    mock_requests_patch.side_effect = requests.ConnectionError("Network connection error")

    url = 'https://api.github.com/repos/user/repo/pulls/1'
    data = 'Updated PR body'
    installation_id = 123

    with pytest.raises(requests.ConnectionError, match="Network connection error"):
        patch_pr_body(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            'Authorization': 'Bearer fake_access_token',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={'body': data}
    )
    mock_logger.debug.assert_not_called()

def test_invalid_url(mock_get_installation_access_token, mock_requests_patch, mock_logger):
    mock_get_installation_access_token.return_value = 'fake_access_token'
    mock_requests_patch.side_effect = requests.RequestException("Invalid URL")

    url = 'invalid_url'
    data = 'Updated PR body'
    installation_id = 123

    with pytest.raises(requests.RequestException, match="Invalid URL"):
        patch_pr_body(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            'Authorization': 'Bearer fake_access_token',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={'body': data}
    )
    mock_logger.debug.assert_not_called()

def test_timeout_error(mock_get_installation_access_token, mock_requests_patch, mock_logger):
    mock_get_installation_access_token.return_value = 'fake_access_token'
    mock_requests_patch.side_effect = requests.Timeout("Timeout error")

    url = 'https://api.github.com/repos/user/repo/pulls/1'
    data = 'Updated PR body'
    installation_id = 123

    with pytest.raises(requests.Timeout, match="Timeout error"):
        patch_pr_body(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            'Authorization': 'Bearer fake_access_token',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={'body': data}
    )
    mock_logger.debug.assert_not_called()

@pytest.mark.parametrize("data", ["a", "a" * 65536, "a" * 65535])
def test_boundary_conditions(data, mock_get_installation_access_token, mock_requests_patch, mock_logger):
    mock_get_installation_access_token.return_value = 'fake_access_token'
    mock_response = Mock()
    mock_response.text = 'Success'
    mock_requests_patch.return_value = mock_response

    url = 'https://api.github.com/repos/user/repo/pulls/1'
    installation_id = 123

    patch_pr_body(url, data, installation_id)

    mock_get_installation_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            'Authorization': 'Bearer fake_access_token',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={'body': data}
    )
    mock_logger.debug.assert_called_once_with('Patch Pull request response: Success')