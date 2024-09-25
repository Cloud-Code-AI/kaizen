import os
import jwt
import time
import requests
import logging
import hmac
import hashlib
from bs4 import BeautifulSoup
from typing import List, Tuple

logger = logging.getLogger(__name__)

# GitHub App configuration
GITHUB_APP_ID = os.environ.get("GITHUB_APP_ID")
GITHUB_APP_WEBHOOK_SECRET = os.environ.get("GITHUB_APP_WEBHOOK_SECRET")


HEADERS = {
    "Authorization": None,
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def is_successful_status(status_code):
    return 200 <= status_code < 300


def generate_jwt():
    # Define the time the JWT was issued and its expiration time
    issued_at_time = int(time.time())
    expiration_time = issued_at_time + (7 * 60)  # JWT expires in 15 minutes

    # Define the JWT payload
    payload = {"iat": issued_at_time, "exp": expiration_time, "iss": GITHUB_APP_ID}
    file_path = os.environ.get("GITHUB_APP_PEM_PATH", "GITHUB_APP_KEY.pem")
    logger.info(f"filepath: {file_path}")
    with open(file_path, "r") as f:
        # Encode the JWT using the RS256 algorithm
        encoded_jwt = jwt.encode(payload, f.read(), algorithm="RS256")
        logger.info(f"f.read(): {f.read()}")
    return encoded_jwt


def get_diff_text(url, access_token):
    headers = {
        "Accept": "application/vnd.github.v3.patch",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    response = requests.get(url, headers=headers)
    if not is_successful_status(response.status_code):
        logger.error(
            f"Unable to fetch PR diff with error: {response.status_code} url: {url}"
        )
        print(response.text)
        return None
    return response.text


def get_pr_files(url, access_token):
    headers = {
        "Accept": "application/vnd.github.v3+json",
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    response = requests.get(url, headers=headers)
    if not is_successful_status(response.status_code):
        logger.error(
            f"Unable to fetch PR files with error: {response.status_code} url: {url}"
        )
        print(response.text)
        return None
    return response.json()


def is_github_signature_valid(headers, body):
    """
    Validate the signature of the incoming request against the secret.
    """
    github_secret = os.environ.get("GITHUB_APP_WEBHOOK_SECRET", "").encode()
    signature = headers.get("X-Hub-Signature-256")

    if not signature or not github_secret:
        return False

    sha_name, signature = signature.split("=")
    if sha_name != "sha256":
        return False

    mac = hmac.new(github_secret, msg=body, digestmod=hashlib.sha256)
    return hmac.compare_digest(mac.hexdigest(), signature)


def scrape_labels(labels_url) -> List[Tuple[str, str]]:
    """
    Scrape the label names and descriptions of a repository
    """
    response = requests.get(labels_url)
    if response.status_code == 200:
        html_content = response.text
    else:
        logger.error(
            f"Unable to fetch labels page with error: {response.status_code} url: {labels_url}"
        )
    soup = BeautifulSoup(html_content, 'html.parser')
    label_elem = soup.find_all('div', class_='js-label-preview')
    label_with_desc = []
    for label in label_elem:
        labels = label.find_all('span', class_='IssueLabel')
        for label in labels:
            name = label.text.strip()
            desc_elem = label.find_text('div')
            desc_str = desc_elem.text.strip()
            label_desc = desc_str if desc_str else "N/A"
            label_with_desc.append((name, label_desc))
    return label_with_desc


def scrape_labels_all_pages(base_label_url) -> List[Tuple[str, str]]:
    all_labels = []
    page_number = 1
    while True:
        url = f"{base_label_url}?page={page_number}"
        _labels = scrape_labels(url)
        if not _labels:
            break
        all_labels += _labels
        page_number += 1
    return all_labels
