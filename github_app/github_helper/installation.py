from github_app.github_helper import utils
import requests
from github_app.github_helper.endpoints import GITHUB_ENDPOINTS


def get_installations():
    headers = utils.HEADERS
    headers["Authorization"] = f"Bearer {utils.generate_jwt()}"
    url = GITHUB_ENDPOINTS["get_installations"]
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_installation_access_token(installation_id, permissions=None):
    headers = utils.HEADERS
    headers["Authorization"] = f"Bearer {utils.generate_jwt()}"
    url = GITHUB_ENDPOINTS["get_installation_access_token"].format(
        installation_id=installation_id
    )
    body = {}
    if permissions:
        body["permissions"] = permissions
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()["token"]
