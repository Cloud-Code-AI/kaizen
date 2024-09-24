import pytest
import requests
from urllib.parse import urljoin

# Set the base URL for the API
base_url = "https://example.com"

# Set the API endpoint path
endpoint_path = "/store/inventory"

# Set the API key for authentication
api_key = "your_api_key_here"

def test_get_inventory_valid_request():
    """
    Test that a valid GET request to /store/inventory returns a successful response
    """
    url = urljoin(base_url, endpoint_path)
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json() is not None

def test_get_inventory_invalid_request_no_api_key():
    """
    Test that a GET request to /store/inventory without an API key returns a 401 response
    """
    url = urljoin(base_url, endpoint_path)
    response = requests.get(url)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_get_inventory_invalid_request_invalid_api_key():
    """
    Test that a GET request to /store/inventory with an invalid API key returns a 401 response
    """
    url = urljoin(base_url, endpoint_path)
    headers = {"Authorization": "Bearer invalid_api_key"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_get_inventory_edge_case_empty_response():
    """
    Test that a GET request to /store/inventory returns an empty response when there is no data
    """
    url = urljoin(base_url, endpoint_path)
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json() == {}

def test_get_inventory_version_compatibility():
    """
    Test that a GET request to /store/inventory returns a successful response with different API versions
    """
    url = urljoin(base_url, endpoint_path)
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/vnd.example.v1+json"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json() is not None

    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/vnd.example.v2+json"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json() is not None