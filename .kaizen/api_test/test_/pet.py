import pytest
import requests
from requests.auth import HTTPBasicAuth

# Test scenario: Add a new pet to the store
@pytest.mark.parametrize("pet_name, pet_status", [
    ("Fido", "available"),
    ("Whiskers", "pending"),
    ("Fluffy", "sold")
])
def test_add_pet_valid_request(pet_name, pet_status):
    # Set up the request body
    pet_data = {
        "name": pet_name,
        "status": pet_status
    }

    # Set up the authentication
    auth = HTTPBasicAuth("username", "password")

    # Send the request
    response = requests.post("/pet", json=pet_data, auth=auth)

    # Check the response status code
    assert response.status_code == 200

    # Check the response content
    assert response.json()["name"] == pet_name
    assert response.json()["status"] == pet_status

# Test invalid request formats
@pytest.mark.parametrize("invalid_request", [
    {"name": "Fido"},  # missing status
    {"status": "available"},  # missing name
    {"name": "Fido", "status": " invalid_status"}  # invalid status
])
def test_add_pet_invalid_request(invalid_request):
    # Set up the authentication
    auth = HTTPBasicAuth("username", "password")

    # Send the request
    response = requests.post("/pet", json=invalid_request, auth=auth)

    # Check the response status code
    assert response.status_code == 405

    # Check the response content
    assert response.json()["message"] == "Invalid input"

# Test edge cases
@pytest.mark.parametrize("edge_case", [
    {"name": "", "status": "available"},  # empty name
    {"name": "Fido", "status": ""}  # empty status
])
def test_add_pet_edge_cases(edge_case):
    # Set up the authentication
    auth = HTTPBasicAuth("username", "password")

    # Send the request
    response = requests.post("/pet", json=edge_case, auth=auth)

    # Check the response status code
    assert response.status_code == 405

    # Check the response content
    assert response.json()["message"] == "Invalid input"

# Test authentication
def test_add_pet_authentication():
    # Set up the request body
    pet_data = {
        "name": "Fido",
        "status": "available"
    }

    # Send the request without authentication
    response = requests.post("/pet", json=pet_data)

    # Check the response status code
    assert response.status_code == 401

    # Check the response content
    assert response.json()["message"] == "Unauthorized"import pytest
import requests
from requests.auth import HTTPBasicAuth

# Test data
pet_id = 1
valid_pet_data = {
    "id": pet_id,
    "name": "Fido",
    "status": "available"
}

invalid_pet_data = {
    "id": " invalid_id",
    "name": "Fido",
    "status": "available"
}

# Authentication data
username = "test_user"
password = "test_password"

def test_update_pet_valid_request():
    response = requests.put(
        f"/pet/{pet_id}",
        json=valid_pet_data,
        auth=HTTPBasicAuth(username, password)
    )
    assert response.status_code == 200
    assert response.json()["id"] == pet_id
    assert response.json()["name"] == "Fido"
    assert response.json()["status"] == "available"

def test_update_pet_invalid_request():
    response = requests.put(
        f"/pet/{pet_id}",
        json=invalid_pet_data,
        auth=HTTPBasicAuth(username, password)
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid ID supplied"

def test_update_pet_not_found():
    response = requests.put(
        f"/pet/999",
        json=valid_pet_data,
        auth=HTTPBasicAuth(username, password)
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Pet not found"

def test_update_pet_validation_exception():
    response = requests.put(
        f"/pet/{pet_id}",
        json={"id": pet_id, "name": "Fido", "status": " invalid_status"},
        auth=HTTPBasicAuth(username, password)
    )
    assert response.status_code == 405
    assert response.json()["message"] == "Validation exception"

def test_update_pet_unauthorized():
    response = requests.put(
        f"/pet/{pet_id}",
        json=valid_pet_data
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_update_pet_invalid_content_type():
    response = requests.put(
        f"/pet/{pet_id}",
        data=" invalid_data",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        auth=HTTPBasicAuth(username, password)
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid request format"