import pytest
import requests
from urllib.parse import urlencode

# Test constants
BASE_URL = "https://petstore.swagger.io/v2"
ENDPOINT = "/pet/findByTags"
VALID_TAGS = ["tag1", "tag2", "tag3"]
INVALID_TAGS = [" invalid_tag", "tag_with_spaces", ""]

# Test scenarios
def test_find_pets_by_tags_valid_request():
    """Test finding pets by tags with a valid request"""
    params = {"tags": VALID_TAGS}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 200
    assert response.json()  # Check if response is not empty

def test_find_pets_by_tags_invalid_request():
    """Test finding pets by tags with an invalid request"""
    params = {"tags": INVALID_TAGS}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid tag value"

def test_find_pets_by_tags_empty_tags():
    """Test finding pets by tags with empty tags"""
    params = {"tags": []}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 200
    assert response.json()  # Check if response is not empty

def test_find_pets_by_tags_no_tags():
    """Test finding pets by tags with no tags"""
    response = requests.get(BASE_URL + ENDPOINT)
    assert response.status_code == 200
    assert response.json()  # Check if response is not empty

def test_find_pets_by_tags_invalid_tag_format():
    """Test finding pets by tags with invalid tag format"""
    params = {"tags": "tag1,tag2,tag3, invalid_tag"}
    response = requests.get(BASE_URL + ENDPOINT, params=params)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid tag value"

def test_find_pets_by_tags_unauthenticated():
    """Test finding pets by tags without authentication"""
    response = requests.get(BASE_URL + ENDPOINT, headers={"Authorization": " invalid_token"})
    assert response.status_code == 401

def test_find_pets_by_tags_version_compatibility():
    """Test finding pets by tags with different API versions"""
    response = requests.get(BASE_URL + "/v1" + ENDPOINT)
    assert response.status_code == 404