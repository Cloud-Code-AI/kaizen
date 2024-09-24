import pytest
import requests
from urllib.parse import urljoin

# Set the base URL for the API
BASE_URL = "http://localhost:8080"

# Set the API endpoint path
ENDPOINT_PATH = "/store/inventory"

# Set the API key for authentication
API_KEY = "your_api_key_here"

def test_get_inventory_valid_request():
    """
    Test that a valid GET request to the /store/inventory endpoint returns a successful response.
    """
    url = urljoin(BASE_URL, ENDPOINT_PATH)
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json() is not None

def test_get_inventory_invalid_request_no_api_key():
    """
    Test that a GET request to the /store/inventory endpoint without an API key returns a 401 Unauthorized response.
    """
    url = urljoin(BASE_URL, ENDPOINT_PATH)
    response = requests.get(url)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_get_inventory_invalid_request_invalid_api_key():
    """
    Test that a GET request to the /store/inventory endpoint with an invalid API key returns a 401 Unauthorized response.
    """
    url = urljoin(BASE_URL, ENDPOINT_PATH)
    headers = {"Authorization": "Bearer invalid_api_key"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_get_inventory_edge_case_empty_response():
    """
    Test that a GET request to the /store/inventory endpoint returns an empty response when there are no inventories.
    """
    url = urljoin(BASE_URL, ENDPOINT_PATH)
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json() == {}

def test_get_inventory_version_compatibility():
    """
    Test that a GET request to the /store/inventory endpoint returns a successful response with different API versions.
    """
    url = urljoin(BASE_URL, ENDPOINT_PATH)
    headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/vnd.api+json; version=1"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json() is not None

    headers = {"Authorization": f"Bearer {API_KEY}", "Accept": "application/vnd.api+json; version=2"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json() is not None