import pytest
import requests

# Import authentication helpers
from auth_helpers import login_user, get_auth_token

# Set API endpoint URL
endpoint_url = "/user/logout"

# Test scenario: Successful logout
def test_logout_success():
    # Login user and get auth token
    token = login_user()
    headers = {"Authorization": f"Bearer {token}"}

    # Send GET request to logout endpoint
    response = requests.get(endpoint_url, headers=headers)

    # Assert successful response
    assert response.status_code == 200
    assert response.json() == {"message": "successful operation"}

# Test scenario: Invalid request format (missing auth token)
def test_logout_invalid_request_format():
    # Send GET request to logout endpoint without auth token
    response = requests.get(endpoint_url)

    # Assert error response
    assert response.status_code == 401
    assert response.json() == {"error": "Unauthorized"}

# Test scenario: Edge case - already logged out user
def test_logout_already_logged_out():
    # Login user and get auth token
    token = login_user()
    headers = {"Authorization": f"Bearer {token}"}

    # Send GET request to logout endpoint
    response = requests.get(endpoint_url, headers=headers)

    # Assert successful response
    assert response.status_code == 200
    assert response.json() == {"message": "successful operation"}

    # Send GET request to logout endpoint again
    response = requests.get(endpoint_url, headers=headers)

    # Assert error response
    assert response.status_code == 401
    assert response.json() == {"error": "Unauthorized"}

# Test scenario: Authentication check
def test_logout_authentication_check():
    # Send GET request to logout endpoint without auth token
    response = requests.get(endpoint_url)

    # Assert error response
    assert response.status_code == 401
    assert response.json() == {"error": "Unauthorized"}

# Test scenario: Version compatibility check
def test_logout_version_compatibility_check():
    # Set API version in headers
    headers = {"Accept-Version": "v1"}

    # Send GET request to logout endpoint
    response = requests.get(endpoint_url, headers=headers)

    # Assert successful response
    assert response.status_code == 200
    assert response.json() == {"message": "successful operation"}