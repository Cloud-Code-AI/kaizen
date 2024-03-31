import os
from urllib.parse import urljoin


GITHUB_API_BASE_URL = os.environ["GITHUB_API_BASE_URL"]
GITHUB_ENDPOINTS = {
    "get_installations": urljoin(GITHUB_API_BASE_URL, "installations"),
    "get_installation_access_token": urljoin(
        GITHUB_API_BASE_URL, "installations/{installation_id}/access_tokens"
    ),
}
