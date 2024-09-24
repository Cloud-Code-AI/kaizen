import pytest
import requests

# Test scenario: Find purchase order by ID

def test_get_order_by_id_valid(requests_mock):
    # Mock the API response
    requests_mock.get('/store/order/1', json={'id': 1, 'petId': 1, 'quantity': 1, 'shipDate': '2022-01-01T12:00:00.000Z', 'status': 'placed', 'complete': False})

    # Send a GET request to the API endpoint
    response = requests.get('/store/order/1')

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response content
    assert response.json()['id'] == 1
    assert response.json()['petId'] == 1
    assert response.json()['quantity'] == 1
    assert response.json()['shipDate'] == '2022-01-01T12:00:00.000Z'
    assert response.json()['status'] == 'placed'
    assert response.json()['complete'] is False

def test_get_order_by_id_invalid_id(requests_mock):
    # Mock the API response
    requests_mock.get('/store/order/abc', status_code=400, json={'message': 'Invalid ID supplied'})

    # Send a GET request to the API endpoint
    response = requests.get('/store/order/abc')

    # Assert the response status code
    assert response.status_code == 400

    # Assert the response content
    assert response.json()['message'] == 'Invalid ID supplied'

def test_get_order_by_id_order_not_found(requests_mock):
    # Mock the API response
    requests_mock.get('/store/order/6', status_code=404, json={'message': 'Order not found'})

    # Send a GET request to the API endpoint
    response = requests.get('/store/order/6')

    # Assert the response status code
    assert response.status_code == 404

    # Assert the response content
    assert response.json()['message'] == 'Order not found'

def test_get_order_by_id_edge_case_id_equal_to_5(requests_mock):
    # Mock the API response
    requests_mock.get('/store/order/5', json={'id': 5, 'petId': 1, 'quantity': 1, 'shipDate': '2022-01-01T12:00:00.000Z', 'status': 'placed', 'complete': False})

    # Send a GET request to the API endpoint
    response = requests.get('/store/order/5')

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response content
    assert response.json()['id'] == 5
    assert response.json()['petId'] == 1
    assert response.json()['quantity'] == 1
    assert response.json()['shipDate'] == '2022-01-01T12:00:00.000Z'
    assert response.json()['status'] == 'placed'
    assert response.json()['complete'] is False

def test_get_order_by_id_edge_case_id_greater_than_10(requests_mock):
    # Mock the API response
    requests_mock.get('/store/order/11', json={'id': 11, 'petId': 1, 'quantity': 1, 'shipDate': '2022-01-01T12:00:00.000Z', 'status': 'placed', 'complete': False})

    # Send a GET request to the API endpoint
    response = requests.get('/store/order/11')

    # Assert the response status code
    assert response.status_code == 200

    # Assert the response content
    assert response.json()['id'] == 11
    assert response.json()['petId'] == 1
    assert response.json()['quantity'] == 1
    assert response.json()['shipDate'] == '2022-01-01T12:00:00.000Z'
    assert response.json()['status'] == 'placed'
    assert response.json()['complete'] is Falseimport pytest
import requests

# Test scenario: Delete purchase order by ID
class TestDeleteOrder:
    def setup_class(self):
        self.base_url = "https://example.com"
        self.endpoint = "/store/order/{orderId}"
        self.valid_order_id = 123
        self.invalid_order_id = "abc"
        self.non_existent_order_id = 1001

    def test_delete_order_valid_id(self):
        # Test with valid order ID
        url = self.base_url + self.endpoint.format(orderId=self.valid_order_id)
        response = requests.delete(url)
        assert response.status_code == 200

    def test_delete_order_invalid_id(self):
        # Test with invalid order ID (non-integer)
        url = self.base_url + self.endpoint.format(orderId=self.invalid_order_id)
        response = requests.delete(url)
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid ID supplied"

    def test_delete_order_non_existent_id(self):
        # Test with non-existent order ID (integer > 1000)
        url = self.base_url + self.endpoint.format(orderId=self.non_existent_order_id)
        response = requests.delete(url)
        assert response.status_code == 404
        assert response.json()["message"] == "Order not found"

    def test_delete_order_empty_id(self):
        # Test with empty order ID
        url = self.base_url + self.endpoint.format(orderId="")
        response = requests.delete(url)
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid ID supplied"

    def test_delete_order_null_id(self):
        # Test with null order ID
        url = self.base_url + self.endpoint.format(orderId=None)
        response = requests.delete(url)
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid ID supplied"

# Run the tests
pytest.main([__file__])