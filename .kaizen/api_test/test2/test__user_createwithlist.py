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
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["username"] == "user1"
    assert response.json()[0]["email"] == "user1@example.com"
    assert response.json()[1]["id"] == 2
    assert response.json()[1]["username"] == "user2"
    assert response.json()[1]["email"] == "user2@example.com"

# Test scenario: Create list of users with invalid input array (missing required fields)
def test_create_users_with_list_invalid_input_missing_fields():
    url = "/user/createWithList"
    payload = [
        {"id": 1, "username": "user1"},
        {"id": 2, "email": "user2@example.com"}
    ]
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    assert response.json()["message"] == "Validation failed"

# Test scenario: Create list of users with invalid input array (invalid data types)
def test_create_users_with_list_invalid_input_invalid_data_types():
    url = "/user/createWithList"
    payload = [
        {"id": "abc", "username": "user1", "email": "user1@example.com"},
        {"id": 2, "username": 123, "email": "user2@example.com"}
    ]
    response = requests.post(url, json=payload)
    assert response.status_code == 400
    assert response.json()["message"] == "Validation failed"

# Test scenario: Create list of users with empty input array
def test_create_users_with_list_empty_input():
    url = "/user/createWithList"
    payload = []
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    assert len(response.json()) == 0

# Test scenario: Create list of users with authentication
def test_create_users_with_list_authentication():
    url = "/user/createWithList"
    payload = [
        {"id": 1, "username": "user1", "email": "user1@example.com"},
        {"id": 2, "username": "user2", "email": "user2@example.com"}
    ]
    headers = {"Authorization": "Bearer valid_token"}
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 2

# Test scenario: Create list of users with invalid authentication
def test_create_users_with_list_invalid_authentication():
    url = "/user/createWithList"
    payload = [
        {"id": 1, "username": "user1", "email": "user1@example.com"},
        {"id": 2, "username": "user2", "email": "user2@example.com"}
    ]
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"