import pytest
from unittest.mock import patch, MagicMock
from github_app.github_helper.pull_requests import process_pull_request, GITHUB_API_BASE_URL

@pytest.fixture
def mock_payload():
    return {
        "pull_request": {
            "comments_url": "https://api.github.com/repos/test/test/issues/1/comments",
            "number": 1,
            "title": "Test PR",
            "body": "This is a test pull request"
        },
        "repository": {
            "full_name": "test/test"
        },
        "installation": {
            "id": 12345
        }
    }

@pytest.fixture
def mock_access_token():
    return "mock_access_token"

@pytest.fixture
def mock_diff_text():
    return "mock diff text"

@pytest.fixture
def mock_pr_files():
    return [{"filename": "test.py", "content": "print('Hello, World!')"}]

@pytest.fixture
def mock_review_data():
    return MagicMock(topics={"important": ["Topic 1", "Topic 2"]})

@patch("github_app.github_helper.pull_requests.get_installation_access_token")
@patch("github_app.github_helper.pull_requests.get_diff_text")
@patch("github_app.github_helper.pull_requests.get_pr_files")
@patch("github_app.github_helper.pull_requests.CodeReviewer")
@patch("github_app.github_helper.pull_requests.clean_keys")
@patch("github_app.github_helper.pull_requests.create_pr_review_text")
@patch("github_app.github_helper.pull_requests.create_review_comments")
@patch("github_app.github_helper.pull_requests.post_pull_request")
@patch("github_app.github_helper.pull_requests.post_pull_request_comments")
def test_process_pull_request_normal_case(
    mock_post_comments, mock_post_pr, mock_create_comments, mock_create_review,
    mock_clean_keys, mock_code_reviewer, mock_get_files, mock_get_diff,
    mock_get_token, mock_payload, mock_access_token, mock_diff_text,
    mock_pr_files, mock_review_data
):
    mock_get_token.return_value = mock_access_token
    mock_get_diff.return_value = mock_diff_text
    mock_get_files.return_value = mock_pr_files
    mock_code_reviewer.return_value.review_pull_request.return_value = mock_review_data
    mock_clean_keys.return_value = ["Topic 1", "Topic 2"]
    mock_create_review.return_value = b"Review description"
    mock_create_comments.return_value = (["Comment 1", "Comment 2"], ["Topic 1", "Topic 2"])

    result, review_desc = process_pull_request(mock_payload)

    assert result is True
    assert review_desc == "Review description"
    mock_post_pr.assert_called_once()
    assert mock_post_comments.call_count == 2

@patch("github_app.github_helper.pull_requests.get_installation_access_token")
@patch("github_app.github_helper.pull_requests.get_diff_text")
@patch("github_app.github_helper.pull_requests.get_pr_files")
@patch("github_app.github_helper.pull_requests.CodeReviewer")
@patch("github_app.github_helper.pull_requests.clean_keys")
@patch("github_app.github_helper.pull_requests.create_pr_review_text")
@patch("github_app.github_helper.pull_requests.create_review_comments")
@patch("github_app.github_helper.pull_requests.post_pull_request")
@patch("github_app.github_helper.pull_requests.post_pull_request_comments")
def test_process_pull_request_cloud_code_ai(
    mock_post_comments, mock_post_pr, mock_create_comments, mock_create_review,
    mock_clean_keys, mock_code_reviewer, mock_get_files, mock_get_diff,
    mock_get_token, mock_payload, mock_access_token, mock_diff_text,
    mock_pr_files, mock_review_data
):
    mock_payload["repository"]["full_name"] = "Cloud-Code-AI"
    mock_get_token.return_value = mock_access_token
    mock_get_diff.return_value = mock_diff_text
    mock_get_files.return_value = mock_pr_files
    mock_code_reviewer.return_value.review_pull_request.return_value = mock_review_data
    mock_clean_keys.return_value = ["Topic 1", "Topic 2"]
    mock_create_review.return_value = b"Review description"
    mock_create_comments.return_value = (["Comment 1", "Comment 2"], ["Topic 1", "Topic 2"])

    with patch("github_app.github_helper.pull_requests.generate_tests") as mock_generate_tests:
        mock_generate_tests.return_value = "Generated tests"
        result, review_desc = process_pull_request(mock_payload)

    assert result is True
    assert review_desc == "Review description"
    mock_post_pr.assert_called_once_with(
        mock_payload["pull_request"]["comments_url"],
        b"Review description",
        mock_payload["installation"]["id"],
        tests="Generated tests"
    )
    assert mock_post_comments.call_count == 2

@pytest.mark.parametrize("diff_text,pr_files", [
    ("", []),
    ("Some diff", []),
    ("", [{"filename": "test.py", "content": "print('Hello')"}]),
])
@patch("github_app.github_helper.pull_requests.get_installation_access_token")
@patch("github_app.github_helper.pull_requests.get_diff_text")
@patch("github_app.github_helper.pull_requests.get_pr_files")
@patch("github_app.github_helper.pull_requests.CodeReviewer")
@patch("github_app.github_helper.pull_requests.clean_keys")
@patch("github_app.github_helper.pull_requests.create_pr_review_text")
@patch("github_app.github_helper.pull_requests.create_review_comments")
@patch("github_app.github_helper.pull_requests.post_pull_request")
@patch("github_app.github_helper.pull_requests.post_pull_request_comments")
def test_process_pull_request_edge_cases(
    mock_post_comments, mock_post_pr, mock_create_comments, mock_create_review,
    mock_clean_keys, mock_code_reviewer, mock_get_files, mock_get_diff,
    mock_get_token, mock_payload, diff_text, pr_files
):
    mock_get_token.return_value = "mock_token"
    mock_get_diff.return_value = diff_text
    mock_get_files.return_value = pr_files
    mock_code_reviewer.return_value.review_pull_request.return_value = MagicMock(topics={})
    mock_clean_keys.return_value = []
    mock_create_review.return_value = b"Review description"
    mock_create_comments.return_value = ([], [])

    result, review_desc = process_pull_request(mock_payload)

    assert result is True
    assert review_desc == "Review description"
    mock_post_pr.assert_called_once()
    mock_post_comments.assert_not_called()

@pytest.mark.parametrize("error_func,error_msg", [
    ("get_installation_access_token", "Failed to get token"),
    ("get_diff_text", "Failed to get diff"),
    ("get_pr_files", "Failed to get PR files"),
    ("CodeReviewer.review_pull_request", "Failed to review PR"),
    ("post_pull_request", "Failed to post PR comment"),
    ("post_pull_request_comments", "Failed to post PR review"),
])
def test_process_pull_request_error_handling(error_func, error_msg, mock_payload):
    with patch(f"github_app.github_helper.pull_requests.{error_func}") as mock_func:
        mock_func.side_effect = Exception(error_msg)
        
        with pytest.raises(Exception) as exc_info:
            process_pull_request(mock_payload)
        
        assert str(exc_info.value) == error_msg

@pytest.mark.parametrize("title,description", [
    ("A" * 1000, "B" * 10000),
    ("Title with unicode: 🚀", "Description with unicode: 😊"),
])
@patch("github_app.github_helper.pull_requests.get_installation_access_token")
@patch("github_app.github_helper.pull_requests.get_diff_text")
@patch("github_app.github_helper.pull_requests.get_pr_files")
@patch("github_app.github_helper.pull_requests.CodeReviewer")
@patch("github_app.github_helper.pull_requests.clean_keys")
@patch("github_app.github_helper.pull_requests.create_pr_review_text")
@patch("github_app.github_helper.pull_requests.create_review_comments")
@patch("github_app.github_helper.pull_requests.post_pull_request")
@patch("github_app.github_helper.pull_requests.post_pull_request_comments")
def test_process_pull_request_boundary_conditions(
    mock_post_comments, mock_post_pr, mock_create_comments, mock_create_review,
    mock_clean_keys, mock_code_reviewer, mock_get_files, mock_get_diff,
    mock_get_token, mock_payload, title, description
):
    mock_payload["pull_request"]["title"] = title
    mock_payload["pull_request"]["body"] = description
    mock_get_token.return_value = "mock_token"
    mock_get_diff.return_value = "mock diff"
    mock_get_files.return_value = [{"filename": f"file_{i}.py", "content": f"print({i})"} for i in range(100)]
    mock_code_reviewer.return_value.review_pull_request.return_value = MagicMock(topics={"important": ["Topic"]})
    mock_clean_keys.return_value = ["Topic"]
    mock_create_review.return_value = b"Review description"
    mock_create_comments.return_value = (["Comment"], ["Topic"])

    result, review_desc = process_pull_request(mock_payload)

    assert result is True
    assert review_desc == "Review description"
    mock_post_pr.assert_called_once()
    mock_post_comments.assert_called_once()

if __name__ == "__main__":
    pytest.main()