import pytest
import requests
from urllib.parse import urlencode

# Test constants
BASE_URL = "https://petstore.swagger.io/v2"
ENDPOINT = "/pet/findByTags"
VALID_TAGS = ["tag1", "tag2", "tag3"]
INVALID_TAGS = [" invalid", "tag with space", ""]
AUTH_TOKEN = "your_auth_token_here"  # Replace with a valid auth token

# Test scenarios
def test_find_pets_by_tags_valid_request():
    """Test finding pets by tags with a valid request"""
    params = {"tags": VALID_TAGS}
    response = requests.get(BASE_URL + ENDPOINT, params=params, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
    assert response.status_code == 200
    assert response.json()  # Check if response is not empty

def test_find_pets_by_tags_invalid_request():
    """Test finding pets by tags with an invalid request"""
    params = {"tags": INVALID_TAGS}
    response = requests.get(BASE_URL + ENDPOINT, params=params, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid tag value"

def test_find_pets_by_tags_empty_tags():
    """Test finding pets by tags with empty tags"""
    params = {"tags": []}
    response = requests.get(BASE_URL + ENDPOINT, params=params, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
    assert response.status_code == 200
    assert response.json() == []  # Check if response is an empty list

def test_find_pets_by_tags_no_auth():
    """Test finding pets by tags without authentication"""
    params = {"tags": VALID_TAGS}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_find_pets_by_tags_invalid_auth():
    """Test finding pets by tags with invalid authentication"""
    params = {"tags": VALID_TAGS}
    response = requests.get(BASE_URL + ENDPOINT, params=params, headers={"Authorization": "Invalid token"})
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_find_pets_by_tags_version_compatibility():
    """Test finding pets by tags with different API versions"""
    params = {"tags": VALID_TAGS}
    response_v2 = requests.get(BASE_URL + ENDPOINT, params=params, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
    response_v3 = requests.get(BASE_URL + "/v3" + ENDPOINT, params=params, headers={"Authorization": f"Bearer {AUTH_TOKEN}"})
    assert response_v2.status_code == response_v3.status_code
    assert response_v2.json() == response_v3.json()