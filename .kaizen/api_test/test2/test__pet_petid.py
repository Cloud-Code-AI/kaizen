import pytest
import requests
from urllib.parse import urljoin

# Set the base URL for the API
BASE_URL = "https://petstore.swagger.io/v2"

# Set the API endpoint path
ENDPOINT_PATH = "/pet/{petId}"

# Define a fixture for a valid pet ID
@pytest.fixture
def valid_pet_id():
    return 1

# Define a fixture for an invalid pet ID
@pytest.fixture
def invalid_pet_id():
    return "abc"

# Define a fixture for a non-existent pet ID
@pytest.fixture
def non_existent_pet_id():
    return 99999

# Test a successful GET request with a valid pet ID
def test_get_pet_by_id_valid(valid_pet_id):
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=valid_pet_id))
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["id"] == valid_pet_id

# Test a GET request with an invalid pet ID
def test_get_pet_by_id_invalid(invalid_pet_id):
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=invalid_pet_id))
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid ID supplied"

# Test a GET request with a non-existent pet ID
def test_get_pet_by_id_non_existent(non_existent_pet_id):
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=non_existent_pet_id))
    response = requests.get(url)
    assert response.status_code == 404
    assert response.json()["message"] == "Pet not found"

# Test authentication
def test_get_pet_by_id_authenticated(valid_pet_id):
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=valid_pet_id))
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200

# Test version compatibility
def test_get_pet_by_id_version_compatibility(valid_pet_id):
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=valid_pet_id))
    headers = {"Accept": "application/vnd.swagger.v2+json"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200import pytest
import requests

# Test scenario: Update a pet in the store with form data

# Test data
pet_id = 1
valid_name = "Fido"
valid_status = "available"
invalid_name = 123  # invalid type
invalid_status = " invalid_status"  # invalid value

# Authentication data
auth_token = "your_auth_token_here"

# API endpoint URL
url = f"/pet/{pet_id}"

# Test functions
def test_update_pet_with_form_valid_request():
    # Set up valid request data
    params = {"name": valid_name, "status": valid_status}
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Send request
    response = requests.post(url, params=params, headers=headers)

    # Assert response status code
    assert response.status_code == 200

def test_update_pet_with_form_invalid_request_name():
    # Set up invalid request data
    params = {"name": invalid_name, "status": valid_status}
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Send request
    response = requests.post(url, params=params, headers=headers)

    # Assert response status code
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

def test_update_pet_with_form_invalid_request_status():
    # Set up invalid request data
    params = {"name": valid_name, "status": invalid_status}
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Send request
    response = requests.post(url, params=params, headers=headers)

    # Assert response status code
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

def test_update_pet_with_form_missing_auth_token():
    # Set up valid request data
    params = {"name": valid_name, "status": valid_status}

    # Send request without auth token
    response = requests.post(url, params=params)

    # Assert response status code
    assert response.status_code == 401

def test_update_pet_with_form_invalid_auth_token():
    # Set up valid request data
    params = {"name": valid_name, "status": valid_status}
    headers = {"Authorization": "Invalid auth token"}

    # Send request with invalid auth token
    response = requests.post(url, params=params, headers=headers)

    # Assert response status code
    assert response.status_code == 401import pytest
import requests
from urllib.parse import urljoin

# Assuming the base URL of the API
BASE_URL = "https://petstore.swagger.io/v2"

# Test scenario: Delete a pet with a valid pet ID
def test_delete_pet_valid_id():
    pet_id = 1  # Assuming a valid pet ID
    api_key = "valid_api_key"  # Assuming a valid API key
    headers = {"api_key": api_key}
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200

# Test scenario: Delete a pet with an invalid pet ID
def test_delete_pet_invalid_id():
    pet_id = "invalid"  # Assuming an invalid pet ID
    api_key = "valid_api_key"  # Assuming a valid API key
    headers = {"api_key": api_key}
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url, headers=headers)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid pet value"

# Test scenario: Delete a pet without an API key
def test_delete_pet_no_api_key():
    pet_id = 1  # Assuming a valid pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

# Test scenario: Delete a pet with an invalid API key
def test_delete_pet_invalid_api_key():
    pet_id = 1  # Assuming a valid pet ID
    api_key = "invalid_api_key"  # Assuming an invalid API key
    headers = {"api_key": api_key}
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url, headers=headers)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

# Edge case: Pet ID is zero
def test_delete_pet_id_zero():
    pet_id = 0
    api_key = "valid_api_key"  # Assuming a valid API key
    headers = {"api_key": api_key}
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url, headers=headers)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid pet value"

# Edge case: Pet ID is negative
def test_delete_pet_id_negative():
    pet_id = -1
    api_key = "valid_api_key"  # Assuming a valid API key
    headers = {"api_key": api_key}
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url, headers=headers)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid pet value"