import pytest
import requests

# Test scenario: Test login functionality with valid and invalid credentials

def test_login_valid_credentials():
    # Test with valid username and password
    url = "/user/login"
    params = {"username": "testuser", "password": "testpassword"}
    response = requests.get(url, params=params)
    assert response.status_code == 200
    assert "X-Rate-Limit" in response.headers
    assert "X-Expires-After" in response.headers
    assert response.json() == "successful operation"

def test_login_invalid_credentials():
    # Test with invalid username and password
    url = "/user/login"
    params = {"username": "invaliduser", "password": "invalidpassword"}
    response = requests.get(url, params=params)
    assert response.status_code == 400
    assert response.json() == "Invalid username/password supplied"

def test_login_missing_credentials():
    # Test with missing username and password
    url = "/user/login"
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json() == "Invalid username/password supplied"

def test_login_empty_credentials():
    # Test with empty username and password
    url = "/user/login"
    params = {"username": "", "password": ""}
    response = requests.get(url, params=params)
    assert response.status_code == 400
    assert response.json() == "Invalid username/password supplied"

def test_login_version_compatibility():
    # Test with different API versions
    url = "/user/login"
    params = {"username": "testuser", "password": "testpassword"}
    response = requests.get(url, params=params, headers={"Accept": "application/vnd.api+json; version=1"})
    assert response.status_code == 200
    response = requests.get(url, params=params, headers={"Accept": "application/vnd.api+json; version=2"})
    assert response.status_code == 200

def test_login_authentication():
    # Test with authentication
    url = "/user/login"
    params = {"username": "testuser", "password": "testpassword"}
    response = requests.get(url, params=params, auth=("testuser", "testpassword"))
    assert response.status_code == 200
    response = requests.get(url, params=params, auth=("invaliduser", "invalidpassword"))
    assert response.status_code == 401