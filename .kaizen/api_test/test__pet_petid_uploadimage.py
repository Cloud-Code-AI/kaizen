import pytest
import requests
from urllib.parse import urljoin

# Assuming the API base URL is defined in a config file or environment variable
BASE_URL = "https://petstore.swagger.io/v2"

def test_upload_image_valid_request():
    pet_id = 1
    image_data = b"image_data"
    additional_metadata = "additional_metadata"

    url = urljoin(BASE_URL, f"/pet/{pet_id}/uploadImage")
    headers = {"Content-Type": "application/octet-stream"}
    params = {"additionalMetadata": additional_metadata}

    response = requests.post(url, headers=headers, params=params, data=image_data)

    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert response.json()["message"] == "File uploaded to /pet/1/uploadImage"

def test_upload_image_invalid_request_no_image_data():
    pet_id = 1
    additional_metadata = "additional_metadata"

    url = urljoin(BASE_URL, f"/pet/{pet_id}/uploadImage")
    headers = {"Content-Type": "application/octet-stream"}
    params = {"additionalMetadata": additional_metadata}

    response = requests.post(url, headers=headers, params=params)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No image data provided"

def test_upload_image_invalid_request_invalid_pet_id():
    pet_id = " invalid_pet_id"
    image_data = b"image_data"
    additional_metadata = "additional_metadata"

    url = urljoin(BASE_URL, f"/pet/{pet_id}/uploadImage")
    headers = {"Content-Type": "application/octet-stream"}
    params = {"additionalMetadata": additional_metadata}

    response = requests.post(url, headers=headers, params=params, data=image_data)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Invalid pet ID"

def test_upload_image_unauthorized():
    pet_id = 1
    image_data = b"image_data"
    additional_metadata = "additional_metadata"

    url = urljoin(BASE_URL, f"/pet/{pet_id}/uploadImage")
    headers = {"Content-Type": "application/octet-stream"}
    params = {"additionalMetadata": additional_metadata}

    response = requests.post(url, headers=headers, params=params, data=image_data)

    assert response.status_code == 401
    assert response.json()["code"] == 401
    assert response.json()["message"] == "Unauthorized"

def test_upload_image_version_incompatibility():
    pet_id = 1
    image_data = b"image_data"
    additional_metadata = "additional_metadata"

    url = urljoin(BASE_URL, f"/pet/{pet_id}/uploadImage")
    headers = {"Content-Type": "application/octet-stream", "Accept-Version": "v1"}
    params = {"additionalMetadata": additional_metadata}

    response = requests.post(url, headers=headers, params=params, data=image_data)

    assert response.status_code == 406
    assert response.json()["code"] == 406
    assert response.json()["message"] == "Version incompatibility"