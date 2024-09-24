import pytest
import requests
import json

# Test scenario: Create list of users with valid input array
def test_create_users_with_list_valid_input():
    url = "/user/createWithList"
    payload = [
        {"id": 1, "username": "user1", "email": "user1@example.com"},
        {"id": 2, "username": "user2", "email": "user2@example.com"}
    ]
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    assert response.status_code == 200
    assert len(response.json()) == 2

# Test scenario: Create list of users with invalid input array (empty array)
def test_create_users_with_list_empty_array():
    url = "/user/createWithList"
    payload = []
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid input array"

# Test scenario: Create list of users with invalid input array (non-array input)
def test_create_users_with_list_non_array_input():
    url = "/user/createWithList"
    payload = {"id": 1, "username": "user1", "email": "user1@example.com"}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid input array"

# Test scenario: Create list of users with invalid input array (missing required fields)
def test_create_users_with_list_missing_required_fields():
    url = "/user/createWithList"
    payload = [
        {"id": 1, "email": "user1@example.com"},
        {"id": 2, "username": "user2"}
    ]
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid input array"

# Test scenario: Create list of users with authentication
def test_create_users_with_list_authentication():
    url = "/user/createWithList"
    payload = [
        {"id": 1, "username": "user1", "email": "user1@example.com"},
        {"id": 2, "username": "user2", "email": "user2@example.com"}
    ]
    headers = {"Content-Type": "application/json", "Authorization": "Bearer token"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    assert response.status_code == 200
    assert len(response.json()) == 2

# Test scenario: Create list of users with version compatibility
def test_create_users_with_list_version_compatibility():
    url = "/user/createWithList"
    payload = [
        {"id": 1, "username": "user1", "email": "user1@example.com"},
        {"id": 2, "username": "user2", "email": "user2@example.com"}
    ]
    headers = {"Content-Type": "application/json", "Accept-Version": "v1"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    assert response.status_code == 200
    assert len(response.json()) == 2