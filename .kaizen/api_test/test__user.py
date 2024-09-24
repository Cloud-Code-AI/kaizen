import pytest
import requests
from requests.auth import HTTPBasicAuth

# Set API endpoint URL
url = "/user"

# Set authentication credentials
username = "test_user"
password = "test_password"

# Define a valid user object
valid_user = {
    "username": "new_user",
    "password": "new_password",
    "email": "new_user@example.com"
}

# Define an invalid user object (missing required field)
invalid_user = {
    "username": "new_user",
    "email": "new_user@example.com"
}

# Test scenario: Create a new user with valid request format
def test_create_user_valid_request():
    response = requests.post(url, json=valid_user, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 201
    assert response.json()["username"] == valid_user["username"]
    assert response.json()["email"] == valid_user["email"]

# Test scenario: Create a new user with invalid request format (missing required field)
def test_create_user_invalid_request():
    response = requests.post(url, json=invalid_user, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid request format"

# Test scenario: Create a new user without authentication
def test_create_user_no_auth():
    response = requests.post(url, json=valid_user)
    assert response.status_code == 401
    assert response.json()["error"] == "Unauthorized"

# Test scenario: Create a new user with invalid authentication credentials
def test_create_user_invalid_auth():
    response = requests.post(url, json=valid_user, auth=HTTPBasicAuth("wrong_username", "wrong_password"))
    assert response.status_code == 401
    assert response.json()["error"] == "Unauthorized"

# Test scenario: Create a new user with duplicate username
def test_create_user_duplicate_username():
    # Create a new user with the same username as an existing user
    response = requests.post(url, json={"username": username, "password": "new_password", "email": "new_email@example.com"}, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 400
    assert response.json()["error"] == "Username already exists"

# Test scenario: Create a new user with invalid email format
def test_create_user_invalid_email():
    response = requests.post(url, json={"username": "new_user", "password": "new_password", "email": "invalid_email"}, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid email format"