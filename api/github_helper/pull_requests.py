from codecheck.actions import reviews


def parse_pull_request(payload):
    comment_url = payload["pull_request"]["comments_url"]
    diff_url = payload["pull_request"]["diff_url"]
    diff_text = get_text_from_html_url(diff_url, access_token)