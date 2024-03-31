import os
import jwt
import time
import requests

# GitHub App configuration
GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITHUB_APP_WEBHOOK_SECRET = os.environ.get('GITHUB_APP_WEBHOOK_SECRET')


HEADER = {
        'Authorization': None,
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

def generate_jwt():
    # Define the time the JWT was issued and its expiration time
    issued_at_time = int(time.time())
    expiration_time = issued_at_time + (7 * 60)  # JWT expires in 15 minutes

    # Define the JWT payload
    payload = {
        'iat': issued_at_time,
        'exp': expiration_time,
        'iss': GITHUB_APP_ID
    }
    with open(".key.pem", "r") as f:
        # Encode the JWT using the RS256 algorithm
        encoded_jwt = jwt.encode(payload, f.read(), algorithm='RS256')
    return encoded_jwt


def get_text_from_html_url(url, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    return response.text