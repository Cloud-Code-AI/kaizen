import os
import jwt
import time
import requests
import logging
import hmac
import hashlib

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
