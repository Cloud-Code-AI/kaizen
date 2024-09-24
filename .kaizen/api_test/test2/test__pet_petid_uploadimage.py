import pytest
import requests
from urllib.parse import urljoin

# Assuming the API base URL is defined in a config file or environment variable
BASE_URL = "https://example.com/api"

def test_upload_image_valid_request():
    # Valid request with required petId and image file
    pet_id = 123
    image_file = open("test_image.jpg", "rb")
    response = requests.post(
        urljoin(BASE_URL, f"/pet/{pet_id}/uploadImage"),
        files={"file": image_file},
        headers={"Content-Type": "application/octet-stream"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "File uploaded successfully"

def test_upload_image_invalid_request_no_pet_id():
    # Invalid request without petId
    response = requests.post(
        urljoin(BASE_URL, "/pet/uploadImage"),
        files={"file": open("test_image.jpg", "rb")},
        headers={"Content-Type": "application/octet-stream"},
    )
    assert response.status_code == 404
    assert response.json()["message"] == "Pet not found"

def test_upload_image_invalid_request_no_image_file():
    # Invalid request without image file
    pet_id = 123
    response = requests.post(
        urljoin(BASE_URL, f"/pet/{pet_id}/uploadImage"),
        headers={"Content-Type": "application/octet-stream"},
    )
    assert response.status_code == 400
    assert response.json()["message"] == "No file provided"

def test_upload_image_invalid_request_invalid_image_file():
    # Invalid request with invalid image file
    pet_id = 123
    response = requests.post(
        urljoin(BASE_URL, f"/pet/{pet_id}/uploadImage"),
        files={"file": open("test_text.txt", "rb")},
        headers={"Content-Type": "application/octet-stream"},
    )
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid file type"

def test_upload_image_additional_metadata():
    # Valid request with additional metadata
    pet_id = 123
    image_file = open("test_image.jpg", "rb")
    response = requests.post(
        urljoin(BASE_URL, f"/pet/{pet_id}/uploadImage"),
        files={"file": image_file},
        headers={"Content-Type": "application/octet-stream"},
        params={"additionalMetadata": "test metadata"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "File uploaded successfully"

def test_upload_image_unauthorized():
    # Unauthorized request without authentication
    pet_id = 123
    image_file = open("test_image.jpg", "rb")
    response = requests.post(
        urljoin(BASE_URL, f"/pet/{pet_id}/uploadImage"),
        files={"file": image_file},
        headers={"Content-Type": "application/octet-stream"},
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Unauthorized"

def test_upload_image_version_compatibility():
    # Test version compatibility by checking the API version in the response
    pet_id = 123
    image_file = open("test_image.jpg", "rb")
    response = requests.post(
        urljoin(BASE_URL, f"/pet/{pet_id}/uploadImage"),
        files={"file": image_file},
        headers={"Content-Type": "application/octet-stream"},
    )
    assert response.status_code == 200
    assert response.json()["apiVersion"] == "1.0.0"