import pytest
import requests
from urllib.parse import urljoin

# Assuming the API base URL is defined in a config file or environment variable
BASE_URL = "https://petstore.swagger.io/v2"

def test_get_pet_by_id_valid_request():
    pet_id = 1  # Replace with a valid pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["id"] == pet_id

def test_get_pet_by_id_invalid_request():
    pet_id = " invalid"  # Invalid pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid ID supplied"

def test_get_pet_by_id_pet_not_found():
    pet_id = 999999  # Non-existent pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.get(url)
    assert response.status_code == 404
    assert response.json()["message"] == "Pet not found"

def test_get_pet_by_id_unauthorized():
    pet_id = 1  # Valid pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.get(url, headers={"Authorization": " invalid"})
    assert response.status_code == 401

def test_get_pet_by_id_edge_case_negative_id():
    pet_id = -1  # Negative pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid ID supplied"

def test_get_pet_by_id_edge_case_zero_id():
    pet_id = 0  # Zero pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid ID supplied"

def test_get_pet_by_id_edge_case_non_integer_id():
    pet_id = "a"  # Non-integer pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid ID supplied"import pytest
import requests
from urllib.parse import urljoin

# Set the base URL for the API
BASE_URL = "https://petstore.swagger.io/v2"

# Set the API endpoint path
ENDPOINT_PATH = "/pet/{petId}"

# Set the authentication credentials
AUTH_USERNAME = "your_username"
AUTH_PASSWORD = "your_password"

# Define a fixture for authentication
@pytest.fixture
def auth_header():
    return {"Authorization": f"Basic {AUTH_USERNAME}:{AUTH_PASSWORD}"}

# Test scenario: Update a pet with valid form data
def test_update_pet_with_form_valid(auth_header):
    pet_id = 1
    name = "Fido"
    status = "available"
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=pet_id))
    response = requests.post(url, headers=auth_header, params={"name": name, "status": status})
    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["status"] == status

# Test scenario: Update a pet with invalid form data (missing name)
def test_update_pet_with_form_invalid_missing_name(auth_header):
    pet_id = 1
    status = "available"
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=pet_id))
    response = requests.post(url, headers=auth_header, params={"status": status})
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

# Test scenario: Update a pet with invalid form data (invalid status)
def test_update_pet_with_form_invalid_status(auth_header):
    pet_id = 1
    name = "Fido"
    status = " invalid_status"
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=pet_id))
    response = requests.post(url, headers=auth_header, params={"name": name, "status": status})
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

# Test scenario: Update a pet with invalid pet ID
def test_update_pet_with_form_invalid_pet_id(auth_header):
    pet_id = " invalid_pet_id"
    name = "Fido"
    status = "available"
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=pet_id))
    response = requests.post(url, headers=auth_header, params={"name": name, "status": status})
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

# Test scenario: Update a pet without authentication
def test_update_pet_with_form_no_auth():
    pet_id = 1
    name = "Fido"
    status = "available"
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=pet_id))
    response = requests.post(url, params={"name": name, "status": status})
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"import pytest
import requests
from urllib.parse import urljoin

# Assuming the base URL of the API
BASE_URL = "https://petstore.swagger.io/v2"

# Test scenario: Delete a pet with valid pet ID and API key
def test_delete_pet_valid_id_and_api_key():
    pet_id = 1  # Replace with a valid pet ID
    api_key = "your_api_key"  # Replace with a valid API key
    headers = {"api_key": api_key}
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200

# Test scenario: Delete a pet with invalid pet ID
def test_delete_pet_invalid_id():
    pet_id = "invalid"  # Invalid pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid pet value"

# Test scenario: Delete a pet without API key
def test_delete_pet_without_api_key():
    pet_id = 1  # Replace with a valid pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url)
    assert response.status_code == 401  # Unauthorized

# Test scenario: Delete a pet with invalid API key
def test_delete_pet_invalid_api_key():
    pet_id = 1  # Replace with a valid pet ID
    api_key = "invalid_api_key"  # Invalid API key
    headers = {"api_key": api_key}
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url, headers=headers)
    assert response.status_code == 401  # Unauthorized

# Edge case: Delete a pet with pet ID as a float
def test_delete_pet_float_id():
    pet_id = 1.1  # Float pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid pet value"

# Edge case: Delete a pet with pet ID as a string
def test_delete_pet_string_id():
    pet_id = "string"  # String pet ID
    url = urljoin(BASE_URL, f"/pet/{pet_id}")
    response = requests.delete(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid pet value"