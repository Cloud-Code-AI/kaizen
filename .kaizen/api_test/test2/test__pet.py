import pytest
import requests
from requests.auth import HTTPBasicAuth

# Test scenario: Add a new pet to the store
@pytest.mark.parametrize("pet_data", [
    {"name": "Fido", "status": "available"},
    {"name": "Whiskers", "status": "pending"},
    {"name": "Fluffy", "status": "sold"}
])
def test_add_pet_valid_request(pet_data):
    response = requests.post("/pet", json=pet_data, auth=HTTPBasicAuth("username", "password"))
    assert response.status_code == 200
    assert response.json()["name"] == pet_data["name"]
    assert response.json()["status"] == pet_data["status"]

# Test invalid request formats
@pytest.mark.parametrize("invalid_data", [
    {"name": "Fido"},  # missing status
    {"status": "available"},  # missing name
    {"name": "Fido", "status": " invalid_status"}  # invalid status
])
def test_add_pet_invalid_request(invalid_data):
    response = requests.post("/pet", json=invalid_data, auth=HTTPBasicAuth("username", "password"))
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

# Test edge cases
def test_add_pet_empty_name():
    response = requests.post("/pet", json={"name": "", "status": "available"}, auth=HTTPBasicAuth("username", "password"))
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

def test_add_pet_empty_status():
    response = requests.post("/pet", json={"name": "Fido", "status": ""}, auth=HTTPBasicAuth("username", "password"))
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

# Test authentication
def test_add_pet_unauthenticated():
    response = requests.post("/pet", json={"name": "Fido", "status": "available"})
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

# Test version compatibility
def test_add_pet_invalid_version():
    response = requests.post("/pet", json={"name": "Fido", "status": "available"}, headers={"Accept-Version": " invalid_version"})
    assert response.status_code == 406
    assert response.json()["message"] == "Not Acceptable"import pytest
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

def test_update_pet_version_compatibility():
    # Assuming the API has a versioning system
    response = requests.put(
        f"/pet/{pet_id}",
        json=valid_pet_data,
        auth=HTTPBasicAuth(username, password),
        headers={"Accept-Version": "v1"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == pet_id
    assert response.json()["name"] == "Fido"
    assert response.json()["status"] == "available"