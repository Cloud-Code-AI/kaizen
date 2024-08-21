import pytest
import requests
from unittest.mock import patch, Mock

# Set up necessary imports
from github_helper.pull_requests import post_pull_request_comments, get_installation_access_token

# Mock external dependencies
@patch('github_helper.pull_requests.get_installation_access_token')
@patch('github_helper.pull_requests.requests.post')
def test_post_pull_request_comments_valid_data(mock_post, mock_get_access_token):
    # Arrange
    url = 'https://api.github.com/repos/owner/repo/pulls/123/comments'
    review = {
        'file_name': 'file.py',
        'start_line': 10,
        'end_line': 15,
        'comment': 'This code needs improvement.'
    }
    installation_id = 1234
    mock_get_access_token.return_value = 'access_token'
    mock_response = Mock()
    mock_response.text = 'Comment posted successfully'
    mock_post.return_value = mock_response

    # Act
    post_pull_request_comments(url, review, installation_id)

    # Assert
    mock_get_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_post.assert_called_once_with(
        url,
        headers={
            'Authorization': 'Bearer access_token',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={
            'event': 'REQUEST_CHANGES',
            'comments': [
                {
                    'path': review['file_name'],
                    'start_line': review['start_line'],
                    'line': review['end_line'],
                    'body': review['comment']
                }
            ]
        }
    )

@patch('github_helper.pull_requests.get_installation_access_token')
@patch('github_helper.pull_requests.requests.post')
def test_post_pull_request_comments_empty_comment(mock_post, mock_get_access_token):
    # Arrange
    url = 'https://api.github.com/repos/owner/repo/pulls/123/comments'
    review = {
        'file_name': 'file.py',
        'start_line': 10,
        'end_line': 15,
        'comment': ''
    }
    installation_id = 1234
    mock_get_access_token.return_value = 'access_token'
    mock_response = Mock()
    mock_response.text = 'Comment posted successfully'
    mock_post.return_value = mock_response

    # Act
    post_pull_request_comments(url, review, installation_id)

    # Assert
    mock_get_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_post.assert_called_once_with(
        url,
        headers={
            'Authorization': 'Bearer access_token',
            'Accept': 'application/vnd.github.v3+json'
        },
        json={
            'event': 'REQUEST_CHANGES',
            'comments': [
                {
                    'path': review['file_name'],
                    'start_line': review['start_line'],
                    'line': review['end_line'],
                    'body': review['comment']
                }
            ]
        }
    )

@patch('github_helper.pull_requests.get_installation_access_token')
@patch('github_helper.pull_requests.requests.post')
def test_post_pull_request_comments_invalid_url(mock_post, mock_get_access_token):
    # Arrange
    url = 'invalid_url'
    review = {
        'file_name': 'file.py',
        'start_line': 10,
        'end_line': 15,
        'comment': 'This code needs improvement.'
    }
    installation_id = 1234
    mock_get_access_token.return_value = 'access_token'
    mock_post.side_effect = requests.exceptions.RequestException('Invalid URL')

    # Act & Assert
    with pytest.raises(requests.exceptions.RequestException):
        post_pull_request_comments(url, review, installation_id)

    mock_get_access_token.assert_called_once_with(installation_id, 'pull_request')

@patch('github_helper.pull_requests.get_installation_access_token')
@patch('github_helper.pull_requests.requests.post')
def test_post_pull_request_comments_no_access_token(mock_post, mock_get_access_token):
    # Arrange
    url = 'https://api.github.com/repos/owner/repo/pulls/123/comments'
    review = {
        'file_name': 'file.py',
        'start_line': 10,
        'end_line': 15,
        'comment': 'This code needs improvement.'
    }
    installation_id = 1234
    mock_get_access_token.return_value = None
    mock_post.side_effect = requests.exceptions.RequestException('No access token')

    # Act & Assert
    with pytest.raises(requests.exceptions.RequestException):
        post_pull_request_comments(url, review, installation_id)

    mock_get_access_token.assert_called_once_with(installation_id, 'pull_request')
    mock_post.assert_not_called()