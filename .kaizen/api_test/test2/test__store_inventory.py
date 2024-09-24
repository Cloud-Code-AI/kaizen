import pytest
import requests
from pytest_httpx import HTTPXMock

# Test scenario: Get pet inventories by status

def test_get_inventory_valid_request(httpx_mock: HTTPXMock):
    # Mock the API response
    httpx_mock.add_response(
        method="GET",
        uri="/store/inventory",
        status_code=200,
        json={"available": 10, "pending": 5, "sold": 20},
    )

    # Send the request
    response = requests.get("/store/inventory")

    # Assert the response
    assert response.status_code == 200
    assert response.json() == {"available": 10, "pending": 5, "sold": 20}

def test_get_inventory_invalid_request(httpx_mock: HTTPXMock):
    # Mock the API response
    httpx_mock.add_response(
        method="GET",
        uri="/store/inventory",
        status_code=400,
        json={"message": "Invalid request"},
    )

    # Send the request with an invalid parameter
    response = requests.get("/store/inventory? invalid_param=123")

    # Assert the response
    assert response.status_code == 400
    assert response.json() == {"message": "Invalid request"}

def test_get_inventory_unauthorized_request(httpx_mock: HTTPXMock):
    # Mock the API response
    httpx_mock.add_response(
        method="GET",
        uri="/store/inventory",
        status_code=401,
        json={"message": "Unauthorized"},
    )

    # Send the request without authentication
    response = requests.get("/store/inventory")

    # Assert the response
    assert response.status_code == 401
    assert response.json() == {"message": "Unauthorized"}

def test_get_inventory_version_incompatibility(httpx_mock: HTTPXMock):
    # Mock the API response
    httpx_mock.add_response(
        method="GET",
        uri="/store/inventory",
        status_code=406,
        json={"message": "Version incompatibility"},
    )

    # Send the request with an incompatible version
    response = requests.get("/store/inventory", headers={"Accept-Version": "1.0.0"})

    # Assert the response
    assert response.status_code == 406
    assert response.json() == {"message": "Version incompatibility"}

def test_get_inventory_edge_case_empty_response(httpx_mock: HTTPXMock):
    # Mock the API response
    httpx_mock.add_response(
        method="GET",
        uri="/store/inventory",
        status_code=200,
        json={},
    )

    # Send the request
    response = requests.get("/store/inventory")

    # Assert the response
    assert response.status_code == 200
    assert response.json() == {}