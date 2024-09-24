import pytest
import requests

# Constants
BASE_URL = "https://example.com"
ENDPOINT = "/user/login"
VALID_USERNAME = "test_user"
VALID_PASSWORD = "test_password"

# Test scenarios
def test_login_valid_credentials():
    """
    Test login with valid username and password
    """
    params = {"username": VALID_USERNAME, "password": VALID_PASSWORD}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 200
    assert "X-Rate-Limit" in response.headers
    assert "X-Expires-After" in response.headers
    assert response.json() == {"message": "successful operation"}

def test_login_invalid_credentials():
    """
    Test login with invalid username and password
    """
    params = {"username": "invalid_user", "password": "invalid_password"}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 400
    assert response.json() == {"message": "Invalid username/password supplied"}

def test_login_missing_username():
    """
    Test login with missing username
    """
    params = {"password": VALID_PASSWORD}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 400
    assert response.json() == {"message": "Invalid username/password supplied"}

def test_login_missing_password():
    """
    Test login with missing password
    """
    params = {"username": VALID_USERNAME}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 400
    assert response.json() == {"message": "Invalid username/password supplied"}

def test_login_empty_username():
    """
    Test login with empty username
    """
    params = {"username": "", "password": VALID_PASSWORD}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 400
    assert response.json() == {"message": "Invalid username/password supplied"}

def test_login_empty_password():
    """
    Test login with empty password
    """
    params = {"username": VALID_USERNAME, "password": ""}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 400
    assert response.json() == {"message": "Invalid username/password supplied"}

# Edge cases
def test_login_username_too_long():
    """
    Test login with username too long
    """
    params = {"username": "a" * 256, "password": VALID_PASSWORD}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 400
    assert response.json() == {"message": "Invalid username/password supplied"}

def test_login_password_too_long():
    """
    Test login with password too long
    """
    params = {"username": VALID_USERNAME, "password": "a" * 256}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 400
    assert response.json() == {"message": "Invalid username/password supplied"}

# Authentication and version compatibility
def test_login_unauthenticated():
    """
    Test login without authentication
    """
    response = requests.get(BASE_URL + ENDPOINT)
    assert response.status_code == 401
    assert response.json() == {"message": "Unauthorized"}

def test_login_incompatible_version():
    """
    Test login with incompatible version
    """
    headers = {"Accept": "application/vnd.example.v1+json"}
    response = requests.get(BASE_URL + ENDPOINT, headers=headers)
    assert response.status_code == 406
    assert response.json() == {"message": "Not Acceptable"}