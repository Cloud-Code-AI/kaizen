import pytest
import requests
from requests.auth import HTTPBasicAuth

# Assuming the API endpoint is hosted on localhost:8080
base_url = "http://localhost:8080"

# Define a fixture for the API client
@pytest.fixture
def client():
    return requests.Session()

# Test scenario: Create a new user with valid request format
def test_create_user_valid_request(client):
    user_data = {"username": "john", "password": "hello", "email": "john@example.com"}
    response = client.post(f"{base_url}/user", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"]
    assert response.json()["email"] == user_data["email"]

# Test scenario: Create a new user with invalid request format (missing required fields)
def test_create_user_invalid_request_missing_fields(client):
    user_data = {"username": "john"}
    response = client.post(f"{base_url}/user", json=user_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid request: missing required fields"

# Test scenario: Create a new user with invalid request format (invalid email)
def test_create_user_invalid_request_invalid_email(client):
    user_data = {"username": "john", "password": "hello", "email": "invalid_email"}
    response = client.post(f"{base_url}/user", json=user_data)
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid request: invalid email"

# Test scenario: Create a new user with authentication
def test_create_user_authenticated(client):
    auth = HTTPBasicAuth("existing_user", "existing_password")
    user_data = {"username": "john", "password": "hello", "email": "john@example.com"}
    response = client.post(f"{base_url}/user", json=user_data, auth=auth)
    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"]
    assert response.json()["email"] == user_data["email"]

# Test scenario: Create a new user with invalid authentication
def test_create_user_invalid_authentication(client):
    auth = HTTPBasicAuth("invalid_user", "invalid_password")
    user_data = {"username": "john", "password": "hello", "email": "john@example.com"}
    response = client.post(f"{base_url}/user", json=user_data, auth=auth)
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid authentication"

# Test scenario: Create a new user with version compatibility
def test_create_user_version_compatibility(client):
    headers = {"Accept": "application/vnd.example.v1+json"}
    user_data = {"username": "john", "password": "hello", "email": "john@example.com"}
    response = client.post(f"{base_url}/user", json=user_data, headers=headers)
    assert response.status_code == 201
    assert response.json()["username"] == user_data["username"]
    assert response.json()["email"] == user_data["email"]