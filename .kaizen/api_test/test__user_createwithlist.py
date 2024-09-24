import pytest
import requests
import json

# Set the API endpoint URL
url = "http://localhost:8080/user/createWithList"

# Define a valid user payload
valid_user_payload = [
    {"id": 1, "username": "user1", "email": "user1@example.com"},
    {"id": 2, "username": "user2", "email": "user2@example.com"}
]

# Define an invalid user payload (missing required fields)
invalid_user_payload = [
    {"id": 1},
    {"username": "user2"}
]

# Define a payload with duplicate users
duplicate_user_payload = [
    {"id": 1, "username": "user1", "email": "user1@example.com"},
    {"id": 1, "username": "user1", "email": "user1@example.com"}
]

# Define a payload with invalid data types
invalid_data_type_payload = [
    {"id": "string", "username": 123, "email": True}
]

def test_create_users_with_list_valid_payload():
    response = requests.post(url, json=valid_user_payload)
    assert response.status_code == 200
    assert len(response.json()) == len(valid_user_payload)

def test_create_users_with_list_invalid_payload():
    response = requests.post(url, json=invalid_user_payload)
    assert response.status_code == 400
    assert "Validation failed" in response.text

def test_create_users_with_list_duplicate_users():
    response = requests.post(url, json=duplicate_user_payload)
    assert response.status_code == 400
    assert "Duplicate users" in response.text

def test_create_users_with_list_invalid_data_types():
    response = requests.post(url, json=invalid_data_type_payload)
    assert response.status_code == 400
    assert "Invalid data types" in response.text

def test_create_users_with_list_empty_payload():
    response = requests.post(url, json=[])
    assert response.status_code == 400
    assert "No users provided" in response.text

def test_create_users_with_list_unauthenticated():
    # Assuming authentication is required for this endpoint
    response = requests.post(url, json=valid_user_payload, headers={"Authorization": "Invalid token"})
    assert response.status_code == 401
    assert "Unauthorized" in response.text

def test_create_users_with_list_version_incompatibility():
    # Assuming versioning is implemented for this endpoint
    response = requests.post(url, json=valid_user_payload, headers={"Accept-Version": "Invalid version"})
    assert response.status_code == 406
    assert "Version not supported" in response.text