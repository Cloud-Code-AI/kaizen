import pytest
import requests

# Test scenario: Find purchase order by ID
class TestGetOrderById:
    def test_valid_id(self):
        # Test with valid ID (integer <= 5 or > 10)
        orderId = 1
        response = requests.get(f"/store/order/{orderId}")
        assert response.status_code == 200
        assert response.json()["id"] == orderId

    def test_invalid_id(self):
        # Test with invalid ID (non-integer or out of range)
        orderId = "abc"
        response = requests.get(f"/store/order/{orderId}")
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid ID supplied"

    def test_order_not_found(self):
        # Test with ID that does not exist
        orderId = 6
        response = requests.get(f"/store/order/{orderId}")
        assert response.status_code == 404
        assert response.json()["message"] == "Order not found"

    def test_edge_case_id_zero(self):
        # Test with ID = 0
        orderId = 0
        response = requests.get(f"/store/order/{orderId}")
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid ID supplied"

    def test_edge_case_id_negative(self):
        # Test with ID < 0
        orderId = -1
        response = requests.get(f"/store/order/{orderId}")
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid ID supplied"

    def test_edge_case_id_non_integer(self):
        # Test with non-integer ID
        orderId = 1.5
        response = requests.get(f"/store/order/{orderId}")
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid ID supplied"

# No authentication or version compatibility checks are applicable for this endpointimport pytest
import requests

# Set the base URL for the API
base_url = "https://example.com"

# Set the API endpoint path
endpoint_path = "/store/order/{orderId}"

# Test scenario: Delete purchase order by ID
def test_delete_order_valid_id():
    # Set a valid order ID
    order_id = 123
    
    # Send the DELETE request
    response = requests.delete(base_url + endpoint_path.format(orderId=order_id))
    
    # Assert that the response status code is 200
    assert response.status_code == 200

def test_delete_order_invalid_id():
    # Set an invalid order ID (non-integer)
    order_id = "abc"
    
    # Send the DELETE request
    response = requests.delete(base_url + endpoint_path.format(orderId=order_id))
    
    # Assert that the response status code is 400
    assert response.status_code == 400
    # Assert that the response contains an error message
    assert "Invalid ID supplied" in response.text

def test_delete_order_id_above_1000():
    # Set an order ID above 1000
    order_id = 1001
    
    # Send the DELETE request
    response = requests.delete(base_url + endpoint_path.format(orderId=order_id))
    
    # Assert that the response status code is 400
    assert response.status_code == 400
    # Assert that the response contains an error message
    assert "Invalid ID supplied" in response.text

def test_delete_order_id_below_1():
    # Set an order ID below 1
    order_id = 0
    
    # Send the DELETE request
    response = requests.delete(base_url + endpoint_path.format(orderId=order_id))
    
    # Assert that the response status code is 400
    assert response.status_code == 400
    # Assert that the response contains an error message
    assert "Invalid ID supplied" in response.text

def test_delete_order_id_not_found():
    # Set an order ID that does not exist
    order_id = 9999
    
    # Send the DELETE request
    response = requests.delete(base_url + endpoint_path.format(orderId=order_id))
    
    # Assert that the response status code is 404
    assert response.status_code == 404
    # Assert that the response contains an error message
    assert "Order not found" in response.text