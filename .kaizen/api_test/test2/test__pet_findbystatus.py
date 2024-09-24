import pytest
import requests
from requests.auth import HTTPBasicAuth

# Test constants
BASE_URL = "https://petstore.swagger.io/v2"
ENDPOINT = "/pet/findByStatus"
VALID_STATUSES = ["available", "pending", "sold"]
INVALID_STATUSES = [" invalid", "status", "123"]

# Test authentication
AUTH_USERNAME = "username"
AUTH_PASSWORD = "password"

def test_find_pets_by_status_valid_request():
    """Test valid request with single status value"""
    status = VALID_STATUSES[0]
    response = requests.get(BASE_URL + ENDPOINT, params={"status": status}, auth=HTTPBasicAuth(AUTH_USERNAME, AUTH_PASSWORD))
    assert response.status_code == 200
    assert response.json()[0]["status"] == status

def test_find_pets_by_status_valid_request_multiple_statuses():
    """Test valid request with multiple status values"""
    statuses = ",".join(VALID_STATUSES)
    response = requests.get(BASE_URL + ENDPOINT, params={"status": statuses}, auth=HTTPBasicAuth(AUTH_USERNAME, AUTH_PASSWORD))
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_find_pets_by_status_invalid_request_invalid_status():
    """Test invalid request with invalid status value"""
    status = INVALID_STATUSES[0]
    response = requests.get(BASE_URL + ENDPOINT, params={"status": status}, auth=HTTPBasicAuth(AUTH_USERNAME, AUTH_PASSWORD))
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid status value"

def test_find_pets_by_status_invalid_request_empty_status():
    """Test invalid request with empty status value"""
    response = requests.get(BASE_URL + ENDPOINT, params={"status": ""}, auth=HTTPBasicAuth(AUTH_USERNAME, AUTH_PASSWORD))
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid status value"

def test_find_pets_by_status_unauthenticated_request():
    """Test unauthenticated request"""
    response = requests.get(BASE_URL + ENDPOINT, params={"status": VALID_STATUSES[0]})
    assert response.status_code == 401

def test_find_pets_by_status_version_incompatibility():
    """Test version incompatibility"""
    response = requests.get(BASE_URL + "/v1" + ENDPOINT, params={"status": VALID_STATUSES[0]}, auth=HTTPBasicAuth(AUTH_USERNAME, AUTH_PASSWORD))
    assert response.status_code == 404