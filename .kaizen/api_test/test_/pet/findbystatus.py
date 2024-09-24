import pytest
import requests
from urllib.parse import urlencode

# Test constants
BASE_URL = "https://petstore.swagger.io/v2"
ENDPOINT = "/pet/findByStatus"
VALID_STATUSES = ["available", "pending", "sold"]
INVALID_STATUSES = [" invalid", "status123", ""]

# Test scenarios
def test_find_pets_by_status_valid_request():
    """Test finding pets by status with a valid request"""
    status = VALID_STATUSES[0]
    params = {"status": status}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 200
    assert response.json()[0]["status"] == status

def test_find_pets_by_status_multiple_statuses():
    """Test finding pets by status with multiple statuses"""
    statuses = ",".join(VALID_STATUSES)
    params = {"status": statuses}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_find_pets_by_status_invalid_status():
    """Test finding pets by status with an invalid status"""
    status = INVALID_STATUSES[0]
    params = {"status": status}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid status value"

def test_find_pets_by_status_empty_status():
    """Test finding pets by status with an empty status"""
    status = ""
    params = {"status": status}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid status value"

def test_find_pets_by_status_no_status():
    """Test finding pets by status with no status"""
    response = requests.get(BASE_URL + ENDPOINT)
    assert response.status_code == 200
    assert len(response.json()) > 0

# Authentication and version compatibility tests
def test_find_pets_by_status_authenticated():
    """Test finding pets by status with authentication"""
    # TODO: implement authentication
    pass

def test_find_pets_by_status_version_compatibility():
    """Test finding pets by status with different API versions"""
    # TODO: implement version compatibility tests
    pass