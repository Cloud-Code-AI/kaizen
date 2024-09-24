import pytest
import requests
from urllib.parse import urljoin

# Assuming the API base URL is defined in a config file or environment variable
BASE_URL = 'https://example.com/api'

def test_upload_image_valid_request():
    # Valid request with required petId and image file
    pet_id = 123
    image_file = open('test_image.jpg', 'rb')
    response = requests.post(
        urljoin(BASE_URL, f'/pet/{pet_id}/uploadImage'),
        files={'file': image_file},
        headers={'Content-Type': 'application/octet-stream'}
    )
    assert response.status_code == 200
    assert response.json()['message'] == 'File uploaded successfully'

def test_upload_image_invalid_request_no_pet_id():
    # Invalid request without petId
    response = requests.post(
        urljoin(BASE_URL, '/pet/uploadImage'),
        files={'file': open('test_image.jpg', 'rb')},
        headers={'Content-Type': 'application/octet-stream'}
    )
    assert response.status_code == 404
    assert response.json()['message'] == 'Pet not found'

def test_upload_image_invalid_request_no_image_file():
    # Invalid request without image file
    pet_id = 123
    response = requests.post(
        urljoin(BASE_URL, f'/pet/{pet_id}/uploadImage'),
        headers={'Content-Type': 'application/octet-stream'}
    )
    assert response.status_code == 400
    assert response.json()['message'] == 'No file provided'

def test_upload_image_invalid_request_invalid_image_file():
    # Invalid request with invalid image file
    pet_id = 123
    image_file = open('test_text.txt', 'rb')
    response = requests.post(
        urljoin(BASE_URL, f'/pet/{pet_id}/uploadImage'),
        files={'file': image_file},
        headers={'Content-Type': 'application/octet-stream'}
    )
    assert response.status_code == 400
    assert response.json()['message'] == 'Invalid file type'

def test_upload_image_edge_case_pet_id_zero():
    # Edge case with petId = 0
    pet_id = 0
    image_file = open('test_image.jpg', 'rb')
    response = requests.post(
        urljoin(BASE_URL, f'/pet/{pet_id}/uploadImage'),
        files={'file': image_file},
        headers={'Content-Type': 'application/octet-stream'}
    )
    assert response.status_code == 404
    assert response.json()['message'] == 'Pet not found'

def test_upload_image_edge_case_pet_id_negative():
    # Edge case with petId < 0
    pet_id = -1
    image_file = open('test_image.jpg', 'rb')
    response = requests.post(
        urljoin(BASE_URL, f'/pet/{pet_id}/uploadImage'),
        files={'file': image_file},
        headers={'Content-Type': 'application/octet-stream'}
    )
    assert response.status_code == 404
    assert response.json()['message'] == 'Pet not found'

def test_upload_image_authentication():
    # Test authentication
    pet_id = 123
    image_file = open('test_image.jpg', 'rb')
    response = requests.post(
        urljoin(BASE_URL, f'/pet/{pet_id}/uploadImage'),
        files={'file': image_file},
        headers={'Content-Type': 'application/octet-stream'},
        auth=('invalid_username', 'invalid_password')
    )
    assert response.status_code == 401
    assert response.json()['message'] == 'Unauthorized'

def test_upload_image_version_compatibility():
    # Test version compatibility
    pet_id = 123
    image_file = open('test_image.jpg', 'rb')
    response = requests.post(
        urljoin(BASE_URL, f'/pet/{pet_id}/uploadImage'),
        files={'file': image_file},
        headers={'Content-Type': 'application/octet-stream', 'Accept-Version': 'v2'}
    )
    assert response.status_code == 200
    assert response.json()['message'] == 'File uploaded successfully'