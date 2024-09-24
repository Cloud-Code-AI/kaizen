import pytest
import requests
from requests.auth import HTTPBasicAuth

# Test data
valid_order = {
    "id": 1,
    "petId": 1,
    "quantity": 1,
    "shipDate": "2023-03-01T12:00:00.000Z",
    "status": "placed",
    "complete": False
}

invalid_order = {
    "id": " invalid",
    "petId": " invalid",
    "quantity": " invalid",
    "shipDate": " invalid",
    "status": " invalid",
    "complete": " invalid"
}

# Test functions
def test_place_order_valid_request():
    response = requests.post("/store/order", json=valid_order)
    assert response.status_code == 200
    assert response.json()["id"] == valid_order["id"]
    assert response.json()["petId"] == valid_order["petId"]
    assert response.json()["quantity"] == valid_order["quantity"]
    assert response.json()["shipDate"] == valid_order["shipDate"]
    assert response.json()["status"] == valid_order["status"]
    assert response.json()["complete"] == valid_order["complete"]

def test_place_order_invalid_request():
    response = requests.post("/store/order", json=invalid_order)
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

def test_place_order_empty_request():
    response = requests.post("/store/order", json={})
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

def test_place_order_invalid_content_type():
    response = requests.post("/store/order", data=" invalid", headers={"Content-Type": "text/plain"})
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

def test_place_order_unauthorized():
    response = requests.post("/store/order", json=valid_order, auth=HTTPBasicAuth("invalid", "invalid"))
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_place_order_version_incompatible():
    response = requests.post("/store/order", json=valid_order, headers={"Accept-Version": " invalid"})
    assert response.status_code == 406
    assert response.json()["message"] == "Version incompatible"