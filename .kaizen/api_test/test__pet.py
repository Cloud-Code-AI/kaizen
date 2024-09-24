import pytest
import requests
from requests.auth import HTTPBasicAuth

# Test data
valid_pet_data = {
    "name": "Fido",
    "status": "available"
}

invalid_pet_data = {
    "name": 123,  # invalid type
    "status": " invalid status"
}

# Authentication credentials
username = "test_user"
password = "test_password"

def test_add_pet_valid_data():
    response = requests.post("/pet", json=valid_pet_data, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200
    assert response.json()["name"] == valid_pet_data["name"]
    assert response.json()["status"] == valid_pet_data["status"]

def test_add_pet_invalid_data():
    response = requests.post("/pet", json=invalid_pet_data, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

def test_add_pet_missing_required_fields():
    response = requests.post("/pet", json={}, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

def test_add_pet_invalid_content_type():
    response = requests.post("/pet", data=" invalid data", headers={"Content-Type": "text/plain"}, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

def test_add_pet_unauthenticated():
    response = requests.post("/pet", json=valid_pet_data)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_add_pet_version_incompatibility():
    # Assuming the API has a versioning system
    response = requests.post("/pet", json=valid_pet_data, headers={"Accept-Version": "v1"}, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 406
    assert response.json()["message"] == "Version not supported"
    
import pytest
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
    # Test valid request with JSON body
    response = requests.put(f"/pet/{pet_id}", json=valid_pet_data, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200
    assert response.json()["id"] == pet_id
    assert response.json()["name"] == "Fido"
    assert response.json()["status"] == "available"

def test_update_pet_invalid_request():
    # Test invalid request with invalid ID
    response = requests.put(f"/pet/{invalid_pet_data['id']}", json=invalid_pet_data, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid ID supplied"

def test_update_pet_not_found():
    # Test request with non-existent pet ID
    response = requests.put(f"/pet/999", json=valid_pet_data, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 404
    assert response.json()["message"] == "Pet not found"

def test_update_pet_validation_exception():
    # Test request with invalid data (e.g. missing required field)
    invalid_data = {"id": pet_id, "name": "Fido"}
    response = requests.put(f"/pet/{pet_id}", json=invalid_data, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 405
    assert response.json()["message"] == "Validation exception"

def test_update_pet_unauthorized():
    # Test request without authentication
    response = requests.put(f"/pet/{pet_id}", json=valid_pet_data)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_update_pet_version_compatibility():
    # Test request with different API version (e.g. using a different Accept header)
    headers = {"Accept": "application/vnd.petstore.v2+json"}
    response = requests.put(f"/pet/{pet_id}", json=valid_pet_data, headers=headers, auth=HTTPBasicAuth(username, password))
    assert response.status_code == 200
    assert response.json()["id"] == pet_id
    assert response.json()["name"] == "Fido"
    assert response.json()["status"] == "available"