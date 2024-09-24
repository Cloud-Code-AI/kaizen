import pytest
import requests
from urllib.parse import urlencode

# Test constants
BASE_URL = "https://example.com/pet"
VALID_TAGS = ["tag1", "tag2", "tag3"]
INVALID_TAGS = [" invalid", "tag with space", ""]

# Test scenarios
def test_find_pets_by_tags_valid_request():
    """Test valid request with multiple tags"""
    params = {"tags": VALID_TAGS}
    response = requests.get(BASE_URL + "/findByTags", params=params)
    assert response.status_code == 200
    assert response.json()  # Check if response is not empty

def test_find_pets_by_tags_single_tag():
    """Test valid request with single tag"""
    params = {"tags": [VALID_TAGS[0]]}
    response = requests.get(BASE_URL + "/findByTags", params=params)
    assert response.status_code == 200
    assert response.json()  # Check if response is not empty

def test_find_pets_by_tags_invalid_tag():
    """Test invalid request with invalid tag"""
    params = {"tags": INVALID_TAGS}
    response = requests.get(BASE_URL + "/findByTags", params=params)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid tag value"

def test_find_pets_by_tags_empty_tags():
    """Test invalid request with empty tags"""
    params = {"tags": []}
    response = requests.get(BASE_URL + "/findByTags", params=params)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid tag value"

def test_find_pets_by_tags_no_tags():
    """Test invalid request with no tags"""
    response = requests.get(BASE_URL + "/findByTags")
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid tag value"

def test_find_pets_by_tags_authentication():
    """Test authentication"""
    # Replace with actual authentication token
    auth_token = "your_auth_token"
    headers = {"Authorization": f"Bearer {auth_token}"}
    params = {"tags": VALID_TAGS}
    response = requests.get(BASE_URL + "/findByTags", headers=headers, params=params)
    assert response.status_code == 200
    assert response.json()  # Check if response is not empty

def test_find_pets_by_tags_version_compatibility():
    """Test version compatibility"""
    # Replace with actual API version
    api_version = "your_api_version"
    headers = {"Accept": f"application/json;version={api_version}"}
    params = {"tags": VALID_TAGS}
    response = requests.get(BASE_URL + "/findByTags", headers=headers, params=params)
    assert response.status_code == 200
    assert response.json()  # Check if response is not empty