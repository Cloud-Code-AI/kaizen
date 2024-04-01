from utils import get_text_from_html_url
from api.github_helper.installation import get_installation_access_token
from codecheck.actions.reviews import review_pull_request


def process_pull_request(payload):
    comment_url = payload["pull_request"]["comments_url"]
    diff_url = payload["pull_request"]["diff_url"]
    installation_id = payload["installation"]["id"]
    pl_title = payload["pull_request"]["title"]
    pl_description = payload["pull_request"]["body"]

    access_token = get_installation_access_token(installation_id)
    diff_text = get_text_from_html_url(diff_url, access_token)
    _ = review_pull_request(
        comment_url=comment_url,
        diff_text=diff_text,
        access_token=access_token,
        pull_request_title=pl_title,
        pull_request_desc=pl_description,
    )
