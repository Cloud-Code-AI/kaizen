import pytest
import requests

# Test scenario: Get user by username
def test_get_user_by_username_valid_request():
    username = "user1"
    response = requests.get(f"/user/{username}")
    assert response.status_code == 200
    assert response.json()["username"] == username

# Test invalid request format: Missing username
def test_get_user_by_username_missing_username():
    response = requests.get("/user/")
    assert response.status_code == 404
    assert response.json()["message"] == "User not found"

# Test invalid request format: Invalid username
def test_get_user_by_username_invalid_username():
    username = " invalid_username"
    response = requests.get(f"/user/{username}")
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username supplied"

# Test edge case: Username with special characters
def test_get_user_by_username_special_characters():
    username = "user!@#$"
    response = requests.get(f"/user/{username}")
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username supplied"

# Test edge case: Username with whitespace
def test_get_user_by_username_whitespace():
    username = "user 1"
    response = requests.get(f"/user/{username}")
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid username supplied"

# Test authentication (assuming authentication is required)
def test_get_user_by_username_unauthenticated():
    username = "user1"
    response = requests.get(f"/user/{username}", headers={"Authorization": "Invalid token"})
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

# Test version compatibility (assuming versioning is used)
def test_get_user_by_username_incompatible_version():
    username = "user1"
    response = requests.get(f"/user/{username}", headers={"Accept-Version": "Invalid version"})
    assert response.status_code == 406
    assert response.json()["message"] == "Not Acceptable"import pytest
import requests
from urllib.parse import urljoin

# Assuming the API base URL is defined in a config file or environment variable
BASE_URL = 'https://api.example.com'

# Define a test user for the tests
TEST_USER = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'password'}

def test_update_user_valid_request():
    # Create a test user
    response = requests.post(urljoin(BASE_URL, '/user'), json=TEST_USER)
    assert response.status_code == 201

    # Update the test user
    updated_user = {'username': 'updated_testuser', 'email': 'updated_testuser@example.com'}
    response = requests.put(urljoin(BASE_URL, f'/user/{TEST_USER["username"]}'), json=updated_user)
    assert response.status_code == 200

    # Verify the user was updated
    response = requests.get(urljoin(BASE_URL, f'/user/{updated_user["username"]}'))
    assert response.status_code == 200
    assert response.json()['username'] == updated_user['username']
    assert response.json()['email'] == updated_user['email']

def test_update_user_invalid_request():
    # Create a test user
    response = requests.post(urljoin(BASE_URL, '/user'), json=TEST_USER)
    assert response.status_code == 201

    # Update the test user with invalid data
    updated_user = {' invalid': 'data'}
    response = requests.put(urljoin(BASE_URL, f'/user/{TEST_USER["username"]}'), json=updated_user)
    assert response.status_code == 400

    # Verify the user was not updated
    response = requests.get(urljoin(BASE_URL, f'/user/{TEST_USER["username"]}'))
    assert response.status_code == 200
    assert response.json()['username'] == TEST_USER['username']
    assert response.json()['email'] == TEST_USER['email']

def test_update_user_non_existent_user():
    # Update a non-existent user
    updated_user = {'username': 'non_existent_user', 'email': 'non_existent_user@example.com'}
    response = requests.put(urljoin(BASE_URL, f'/user/{updated_user["username"]}'), json=updated_user)
    assert response.status_code == 404

def test_update_user_unauthenticated():
    # Update a user without authentication
    updated_user = {'username': 'testuser', 'email': 'testuser@example.com'}
    response = requests.put(urljoin(BASE_URL, f'/user/{updated_user["username"]}'), json=updated_user)
    assert response.status_code == 401

def test_update_user_version_incompatibility():
    # Update a user with an incompatible version
    updated_user = {'username': 'testuser', 'email': 'testuser@example.com'}
    headers = {'Accept': 'application/vnd.example.v1+json'}
    response = requests.put(urljoin(BASE_URL, f'/user/{updated_user["username"]}'), json=updated_user, headers=headers)
    assert response.status_code == 406import pytest
import requests

# Assuming the API endpoint is hosted on localhost
BASE_URL = "http://localhost"

# Test cases for the DELETE /user/{username} endpoint
class TestDeleteUser:
    def test_delete_user_valid_request(self, username="test_user"):
        # Assuming a valid user exists with the given username
        response = requests.delete(f"{BASE_URL}/user/{username}")
        assert response.status_code == 200

    def test_delete_user_invalid_username(self, username=" invalid_user"):
        response = requests.delete(f"{BASE_URL}/user/{username}")
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid username supplied"

    def test_delete_user_non_existent_user(self, username="non_existent_user"):
        response = requests.delete(f"{BASE_URL}/user/{username}")
        assert response.status_code == 404
        assert response.json()["message"] == "User not found"

    def test_delete_user_empty_username(self):
        response = requests.delete(f"{BASE_URL}/user/")
        assert response.status_code == 404

    def test_delete_user_unauthenticated(self, username="test_user"):
        # Assuming authentication is required for this endpoint
        response = requests.delete(f"{BASE_URL}/user/{username}", headers={"Authorization": "Invalid token"})
        assert response.status_code == 401

    def test_delete_user_version_incompatibility(self, username="test_user"):
        # Assuming version incompatibility is handled by the API
        response = requests.delete(f"{BASE_URL}/user/{username}", headers={"Accept-Version": "Invalid version"})
        assert response.status_code == 406

# Test cases for edge cases
class TestDeleteUserEdgeCases:
    def test_delete_user_username_with_special_characters(self, username="test_user!@#$"):
        response = requests.delete(f"{BASE_URL}/user/{username}")
        assert response.status_code == 400

    def test_delete_user_username_with_spaces(self, username="test user"):
        response = requests.delete(f"{BASE_URL}/user/{username}")
        assert response.status_code == 400

    def test_delete_user_username_with_numbers(self, username="test_user123"):
        response = requests.delete(f"{BASE_URL}/user/{username}")
        assert response.status_code == 200