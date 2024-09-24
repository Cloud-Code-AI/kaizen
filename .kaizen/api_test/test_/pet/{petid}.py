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

# Test scenario: Get a pet by ID with a valid request
def test_get_pet_by_id_valid_request(valid_pet_id):
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=valid_pet_id))
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json()["id"] == valid_pet_id

# Test scenario: Get a pet by ID with an invalid request (invalid pet ID)
def test_get_pet_by_id_invalid_request(invalid_pet_id):
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=invalid_pet_id))
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid ID supplied"

# Test scenario: Get a pet by ID with an invalid request (missing pet ID)
def test_get_pet_by_id_missing_pet_id():
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=""))
    response = requests.get(url)
    assert response.status_code == 404
    assert response.json()["message"] == "Pet not found"

# Test scenario: Get a pet by ID with an invalid request (non-integer pet ID)
def test_get_pet_by_id_non_integer_pet_id():
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId="1.5"))
    response = requests.get(url)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid ID supplied"

# Test scenario: Get a pet by ID with authentication
def test_get_pet_by_id_with_authentication(valid_pet_id):
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=valid_pet_id))
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == valid_pet_id

# Test scenario: Get a pet by ID with version compatibility
def test_get_pet_by_id_with_version_compatibility(valid_pet_id):
    url = urljoin(BASE_URL, ENDPOINT_PATH.format(petId=valid_pet_id))
    headers = {"Accept": "application/vnd.swagger.v2+json"}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == valid_pet_idimport pytest
import requests
from urllib.parse import urlencode

# Test constants
PET_ID = 123
NAME = "Fido"
STATUS = "available"

# Test scenario: Update a pet with valid form data
def test_update_pet_with_form_valid_data(petstore_url, auth_token):
    url = f"{petstore_url}/pet/{PET_ID}"
    params = {"name": NAME, "status": STATUS}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(url, params=params, headers=headers)
    assert response.status_code == 200

# Test scenario: Update a pet with invalid form data (missing name)
def test_update_pet_with_form_invalid_data_missing_name(petstore_url, auth_token):
    url = f"{petstore_url}/pet/{PET_ID}"
    params = {"status": STATUS}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(url, params=params, headers=headers)
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

# Test scenario: Update a pet with invalid form data (invalid status)
def test_update_pet_with_form_invalid_data_invalid_status(petstore_url, auth_token):
    url = f"{petstore_url}/pet/{PET_ID}"
    params = {"name": NAME, "status": " invalid"}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(url, params=params, headers=headers)
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

# Test scenario: Update a pet with invalid pet ID
def test_update_pet_with_form_invalid_pet_id(petstore_url, auth_token):
    url = f"{petstore_url}/pet/abc"
    params = {"name": NAME, "status": STATUS}
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(url, params=params, headers=headers)
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

# Test scenario: Update a pet without authentication
def test_update_pet_with_form_no_auth(petstore_url):
    url = f"{petstore_url}/pet/{PET_ID}"
    params = {"name": NAME, "status": STATUS}
    response = requests.post(url, params=params)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

@pytest.fixture
def petstore_url():
    return "https://petstore.swagger.io/v2"

@pytest.fixture
def auth_token():
    # Replace with actual authentication token
    return "your_auth_token_here"import pytest
import requests

# Test scenario: Delete a pet by ID

# Test case 1: Valid request format
def test_delete_pet_valid_request(pet_id):
    url = f"/pet/{pet_id}"
    headers = {"api_key": "valid_api_key"}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200

# Test case 2: Invalid request format - missing pet ID
def test_delete_pet_missing_pet_id():
    url = "/pet/"
    headers = {"api_key": "valid_api_key"}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 404
    assert response.json()["message"] == "Pet not found"

# Test case 3: Invalid request format - invalid pet ID
def test_delete_pet_invalid_pet_id():
    url = "/pet/abc"
    headers = {"api_key": "valid_api_key"}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid pet value"

# Test case 4: Authentication failure
def test_delete_pet_auth_failure(pet_id):
    url = f"/pet/{pet_id}"
    headers = {"api_key": "invalid_api_key"}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

# Test case 5: Edge case - pet ID is 0
def test_delete_pet_edge_case_zero_pet_id():
    url = "/pet/0"
    headers = {"api_key": "valid_api_key"}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid pet value"

# Test case 6: Edge case - pet ID is negative
def test_delete_pet_edge_case_negative_pet_id():
    url = "/pet/-1"
    headers = {"api_key": "valid_api_key"}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid pet value"

# Test case 7: Version compatibility
def test_delete_pet_version_compatibility(pet_id):
    url = f"/pet/{pet_id}"
    headers = {"api_key": "valid_api_key", "Accept": "application/json; version=1.0"}
    response = requests.delete(url, headers=headers)
    assert response.status_code == 200

@pytest.fixture
def pet_id():
    # Create a pet and return its ID
    url = "/pet"
    data = {"name": "Test Pet", "status": "available"}
    response = requests.post(url, json=data)
    return response.json()["id"]