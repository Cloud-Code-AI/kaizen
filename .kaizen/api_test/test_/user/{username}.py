import pytest
import requests

# Set the base URL for the API
base_url = "https://api.example.com"

# Set the API endpoint path
endpoint_path = "/user/{username}"

# Define a fixture for a valid username
@pytest.fixture
def valid_username():
    return "user1"

# Define a fixture for an invalid username
@pytest.fixture
def invalid_username():
    return " invalid_user"

# Test scenario: Get user by valid username
def test_get_user_by_valid_username(valid_username):
    url = base_url + endpoint_path.format(username=valid_username)
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["username"] == valid_username

# Test scenario: Get user by invalid username
def test_get_user_by_invalid_username(invalid_username):
    url = base_url + endpoint_path.format(username=invalid_username)
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username supplied"

# Test scenario: Get user by non-existent username
def test_get_user_by_non_existent_username():
    url = base_url + endpoint_path.format(username="non_existent_user")
    response = requests.get(url)
    assert response.status_code == 404
    assert response.json()["message"] == "User not found"

# Test scenario: Get user by username with special characters
def test_get_user_by_username_with_special_characters():
    url = base_url + endpoint_path.format(username="user!@#$%^&*()")
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username supplied"

# Test scenario: Get user by username with whitespace
def test_get_user_by_username_with_whitespace():
    url = base_url + endpoint_path.format(username=" user with whitespace ")
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username supplied"

# Test scenario: Get user by empty username
def test_get_user_by_empty_username():
    url = base_url + endpoint_path.format(username="")
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username supplied"

# Test scenario: Get user by username with authentication
def test_get_user_by_username_with_authentication(valid_username):
    # Set authentication headers
    headers = {"Authorization": "Bearer your_access_token"}
    url = base_url + endpoint_path.format(username=valid_username)
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == valid_username

# Test scenario: Get user by username with invalid authentication
def test_get_user_by_username_with_invalid_authentication(valid_username):
    # Set invalid authentication headers
    headers = {"Authorization": "Bearer invalid_access_token"}
    url = base_url + endpoint_path.format(username=valid_username)
    response = requests.get(url, headers=headers)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"import pytest
import requests
from urllib.parse import urljoin

# Assuming the API base URL is defined in a config file or environment variable
BASE_URL = "https://api.example.com"

def test_update_user_valid_request():
    username = "testuser"
    user_data = {"id": 1, "username": username, "email": "testuser@example.com"}
    response = requests.put(urljoin(BASE_URL, f"user/{username}"), json=user_data)
    assert response.status_code == 200
    assert response.json()["message"] == "successful operation"

def test_update_user_invalid_request_format():
    username = "testuser"
    user_data = " invalid json data "
    response = requests.put(urljoin(BASE_URL, f"user/{username}"), data=user_data)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid request format"

def test_update_user_missing_required_field():
    username = "testuser"
    user_data = {"id": 1, "email": "testuser@example.com"}
    response = requests.put(urljoin(BASE_URL, f"user/{username}"), json=user_data)
    assert response.status_code == 400
    assert response.json()["message"] == "Missing required field: username"

def test_update_user_invalid_username():
    username = " invalid username "
    user_data = {"id": 1, "username": username, "email": "testuser@example.com"}
    response = requests.put(urljoin(BASE_URL, f"user/{username}"), json=user_data)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username"

def test_update_user_unauthenticated():
    username = "testuser"
    user_data = {"id": 1, "username": username, "email": "testuser@example.com"}
    response = requests.put(urljoin(BASE_URL, f"user/{username}"), json=user_data)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_update_user_version_incompatibility():
    username = "testuser"
    user_data = {"id": 1, "username": username, "email": "testuser@example.com"}
    headers = {"Accept": "application/vnd.example.v1+json"}
    response = requests.put(urljoin(BASE_URL, f"user/{username}"), json=user_data, headers=headers)
    assert response.status_code == 406
    assert response.json()["message"] == "Version incompatibility"

def test_update_user_edge_case_empty_username():
    username = ""
    user_data = {"id": 1, "username": username, "email": "testuser@example.com"}
    response = requests.put(urljoin(BASE_URL, f"user/{username}"), json=user_data)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username"

def test_update_user_edge_case_null_username():
    username = None
    user_data = {"id": 1, "username": username, "email": "testuser@example.com"}
    response = requests.put(urljoin(BASE_URL, f"user/{username}"), json=user_data)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username"import pytest
import requests
from requests.auth import HTTPBasicAuth

# Test constants
BASE_URL = "https://api.example.com"
USERNAME = "testuser"
PASSWORD = "testpassword"

# Test scenarios
def test_delete_user_valid_request():
    # Arrange
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    url = f"{BASE_URL}/user/{USERNAME}"

    # Act
    response = requests.delete(url, auth=auth)

    # Assert
    assert response.status_code == 200

def test_delete_user_invalid_username():
    # Arrange
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    url = f"{BASE_URL}/user/ invalid_username"

    # Act
    response = requests.delete(url, auth=auth)

    # Assert
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username supplied"

def test_delete_user_user_not_found():
    # Arrange
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    url = f"{BASE_URL}/user/nonexistentuser"

    # Act
    response = requests.delete(url, auth=auth)

    # Assert
    assert response.status_code == 404
    assert response.json()["message"] == "User not found"

def test_delete_user_unauthenticated():
    # Arrange
    url = f"{BASE_URL}/user/{USERNAME}"

    # Act
    response = requests.delete(url)

    # Assert
    assert response.status_code == 401

def test_delete_user_empty_username():
    # Arrange
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    url = f"{BASE_URL}/user/"

    # Act
    response = requests.delete(url, auth=auth)

    # Assert
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username supplied"

def test_delete_user_whitespace_username():
    # Arrange
    auth = HTTPBasicAuth(USERNAME, PASSWORD)
    url = f"{BASE_URL}/user/   "

    # Act
    response = requests.delete(url, auth=auth)

    # Assert
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username supplied"