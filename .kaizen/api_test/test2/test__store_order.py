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
    "id": " invalid_id",
    "petId": " invalid_petId",
    "quantity": " invalid_quantity",
    "shipDate": " invalid_shipDate",
    "status": " invalid_status",
    "complete": " invalid_complete"
}

# Test scenarios
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

def test_place_order_empty_request_body():
    response = requests.post("/store/order", json={})
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

def test_place_order_invalid_content_type():
    response = requests.post("/store/order", data=valid_order, headers={"Content-Type": "text/plain"})
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"

def test_place_order_unauthenticated():
    response = requests.post("/store/order", json=valid_order)
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_place_order_version_incompatibility():
    response = requests.post("/store/order", json=valid_order, headers={"Accept-Version": "v2"})
    assert response.status_code == 406
    assert response.json()["message"] == "Not Acceptable"

# Edge cases
def test_place_order_petId_not_found():
    valid_order["petId"] = 999
    response = requests.post("/store/order", json=valid_order)
    assert response.status_code == 404
    assert response.json()["message"] == "Pet not found"

def test_place_order_quantity_zero():
    valid_order["quantity"] = 0
    response = requests.post("/store/order", json=valid_order)
    assert response.status_code == 405
    assert response.json()["message"] == "Invalid input"