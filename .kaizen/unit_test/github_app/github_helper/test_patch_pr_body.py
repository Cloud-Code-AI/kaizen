import pytest
import requests
from unittest.mock import patch, MagicMock

# Assuming the function is located in the following path
from /tmp/tmpn_ihnj4m/github_app/github_helper.pull_requests import patch_pr_body

# Mocking the get_installation_access_token function
def mock_get_installation_access_token(installation_id, permission):
    if installation_id == "invalid":
        return "invalid_token"
    return "valid_token"

@pytest.fixture
def mock_requests_patch():
    with patch("requests.patch") as mock_patch:
        yield mock_patch

@pytest.fixture
def mock_get_token():
    with patch("/tmp/tmpn_ihnj4m/github_app/github_helper.pull_requests.get_installation_access_token", side_effect=mock_get_installation_access_token):
        yield

def test_patch_pr_body_valid(mock_requests_patch, mock_get_token):
    url = "https://api.github.com/repos/user/repo/pulls/1"
    data = "Updated PR body"
    installation_id = "valid_id"
    
    mock_response = MagicMock()
    mock_response.text = "Success"
    mock_requests_patch.return_value = mock_response
    
    patch_pr_body(url, data, installation_id)
    
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            "Authorization": "Bearer valid_token",
            "Accept": "application/vnd.github.v3+json",
        },
        json={"body": data}
    )

def test_patch_pr_body_empty_data(mock_requests_patch, mock_get_token):
    url = "https://api.github.com/repos/user/repo/pulls/1"
    data = ""
    installation_id = "valid_id"
    
    mock_response = MagicMock()
    mock_response.text = "Success"
    mock_requests_patch.return_value = mock_response
    
    patch_pr_body(url, data, installation_id)
    
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            "Authorization": "Bearer valid_token",
            "Accept": "application/vnd.github.v3+json",
        },
        json={"body": data}
    )

def test_patch_pr_body_invalid_url(mock_requests_patch, mock_get_token):
    url = "invalid_url"
    data = "Updated PR body"
    installation_id = "valid_id"
    
    mock_response = MagicMock()
    mock_response.text = "Not Found"
    mock_response.status_code = 404
    mock_requests_patch.return_value = mock_response
    
    patch_pr_body(url, data, installation_id)
    
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            "Authorization": "Bearer valid_token",
            "Accept": "application/vnd.github.v3+json",
        },
        json={"body": data}
    )

def test_patch_pr_body_invalid_token(mock_requests_patch, mock_get_token):
    url = "https://api.github.com/repos/user/repo/pulls/1"
    data = "Updated PR body"
    installation_id = "invalid"
    
    mock_response = MagicMock()
    mock_response.text = "Unauthorized"
    mock_response.status_code = 401
    mock_requests_patch.return_value = mock_response
    
    patch_pr_body(url, data, installation_id)
    
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            "Authorization": "Bearer invalid_token",
            "Accept": "application/vnd.github.v3+json",
        },
        json={"body": data}
    )

def test_patch_pr_body_network_error(mock_requests_patch, mock_get_token):
    url = "https://api.github.com/repos/user/repo/pulls/1"
    data = "Updated PR body"
    installation_id = "valid_id"
    
    mock_requests_patch.side_effect = requests.exceptions.ConnectionError
    
    with pytest.raises(requests.exceptions.ConnectionError):
        patch_pr_body(url, data, installation_id)
    
    mock_requests_patch.assert_called_once_with(
        url,
        headers={
            "Authorization": "Bearer valid_token",
            "Accept": "application/vnd.github.v3+json",
        },
        json={"body": data}
    )