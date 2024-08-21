import pytest
from unittest.mock import patch, Mock
from github_app.github_helper.pull_requests import process_pr_desc

# Fixtures
@pytest.fixture
def valid_payload():
    return {
        "pull_request": {
            "url": "https://api.github.com/repos/owner/repo/pulls/123",
            "number": 123,
            "title": "Pull Request Title",
            "body": "Pull Request Description",
        },
        "repository": {"full_name": "owner/repo"},
        "installation": {"id": 1234},
    }

@pytest.fixture
def no_description_payload(valid_payload):
    payload = valid_payload.copy()
    payload["pull_request"]["body"] = ""
    return payload

@pytest.fixture
def no_files_changed_payload(valid_payload):
    return valid_payload

@pytest.fixture
def missing_fields_payload():
    return {
        "pull_request": {
            "url": "https://api.github.com/repos/owner/repo/pulls/123",
            "number": 123,
            "title": "Pull Request Title",
        },
        "repository": {"full_name": "owner/repo"},
    }

@pytest.fixture
def long_title_payload(valid_payload):
    payload = valid_payload.copy()
    payload["pull_request"]["title"] = "Very Long Title " * 100
    return payload

@pytest.fixture
def many_files_changed_payload(valid_payload):
    payload = valid_payload.copy()
    payload["pull_request"]["files"] = [{"filename": f"file{i}.py"} for i in range(1000)]
    return payload

# Test cases
def test_process_pr_desc_valid_payload(valid_payload, monkeypatch):
    # Mock dependencies
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_installation_access_token", Mock(return_value="token"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_pr_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.sort_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_diff_text", Mock(return_value="diff"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.PRDescriptionGenerator.generate_pull_request_desc", Mock(return_value=Mock(desc="generated description")))
    monkeypatch.setattr("github_app.github_helper.pull_requests.patch_pr_body", Mock())

    process_pr_desc(valid_payload)

    # Assert that patch_pr_body was called with the expected arguments
    github_app.github_helper.pull_requests.patch_pr_body.assert_called_with(
        "https://api.github.com/repos/owner/repo/pulls/123",
        "generated description",
        1234,
    )

def test_process_pr_desc_no_description(no_description_payload, monkeypatch):
    # Mock dependencies
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_installation_access_token", Mock(return_value="token"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_pr_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.sort_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_diff_text", Mock(return_value="diff"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.PRDescriptionGenerator.generate_pull_request_desc", Mock(return_value=Mock(desc="generated description")))
    monkeypatch.setattr("github_app.github_helper.pull_requests.patch_pr_body", Mock())

    process_pr_desc(no_description_payload)

    # Assert that patch_pr_body was called with the expected arguments
    github_app.github_helper.pull_requests.patch_pr_body.assert_called_with(
        "https://api.github.com/repos/owner/repo/pulls/123",
        "generated description",
        1234,
    )

def test_process_pr_desc_no_files_changed(no_files_changed_payload, monkeypatch):
    # Mock dependencies
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_installation_access_token", Mock(return_value="token"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_pr_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.sort_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_diff_text", Mock(return_value="diff"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.PRDescriptionGenerator.generate_pull_request_desc", Mock(return_value=Mock(desc="generated description")))
    monkeypatch.setattr("github_app.github_helper.pull_requests.patch_pr_body", Mock())

    process_pr_desc(no_files_changed_payload)

    # Assert that patch_pr_body was called with the expected arguments
    github_app.github_helper.pull_requests.patch_pr_body.assert_called_with(
        "https://api.github.com/repos/owner/repo/pulls/123",
        "generated description",
        1234,
    )

def test_process_pr_desc_missing_fields(missing_fields_payload):
    with pytest.raises(KeyError):
        process_pr_desc(missing_fields_payload)

def test_process_pr_desc_long_title(long_title_payload, monkeypatch):
    # Mock dependencies
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_installation_access_token", Mock(return_value="token"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_pr_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.sort_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_diff_text", Mock(return_value="diff"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.PRDescriptionGenerator.generate_pull_request_desc", Mock(return_value=Mock(desc="generated description")))
    monkeypatch.setattr("github_app.github_helper.pull_requests.patch_pr_body", Mock())

    process_pr_desc(long_title_payload)

    # Assert that patch_pr_body was called with the expected arguments
    github_app.github_helper.pull_requests.patch_pr_body.assert_called_with(
        "https://api.github.com/repos/owner/repo/pulls/123",
        "generated description",
        1234,
    )

def test_process_pr_desc_many_files_changed(many_files_changed_payload, monkeypatch):
    # Mock dependencies
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_installation_access_token", Mock(return_value="token"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_pr_files", Mock(return_value=[{"filename": f"file{i}.py"} for i in range(1000)]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.sort_files", Mock(return_value=[{"filename": f"file{i}.py"} for i in range(1000)]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_diff_text", Mock(return_value="diff"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.PRDescriptionGenerator.generate_pull_request_desc", Mock(return_value=Mock(desc="generated description")))
    monkeypatch.setattr("github_app.github_helper.pull_requests.patch_pr_body", Mock())

    process_pr_desc(many_files_changed_payload)

    # Assert that patch_pr_body was called with the expected arguments
    github_app.github_helper.pull_requests.patch_pr_body.assert_called_with(
        "https://api.github.com/repos/owner/repo/pulls/123",
        "generated description",
        1234,
    )

@pytest.mark.parametrize(
    "error_mock, expected_exception",
    [
        ("get_installation_access_token", Exception),
        ("get_pr_files", Exception),
        ("get_diff_text", Exception),
        ("PRDescriptionGenerator.generate_pull_request_desc", Exception),
        ("patch_pr_body", Exception),
    ],
)
def test_process_pr_desc_error_handling(valid_payload, monkeypatch, error_mock, expected_exception):
    # Mock dependencies
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_installation_access_token", Mock(return_value="token"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_pr_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.sort_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_diff_text", Mock(return_value="diff"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.PRDescriptionGenerator.generate_pull_request_desc", Mock(return_value=Mock(desc="generated description")))
    monkeypatch.setattr("github_app.github_helper.pull_requests.patch_pr_body", Mock())

    # Raise an exception for the specified mock
    monkeypatch.setattr(f"github_app.github_helper.pull_requests.{error_mock}", Mock(side_effect=Exception))

    with pytest.raises(expected_exception):
        process_pr_desc(valid_payload)

def test_process_pr_desc_empty_payload():
    with pytest.raises(TypeError):
        process_pr_desc({})

def test_process_pr_desc_no_title(valid_payload, monkeypatch):
    # Mock dependencies
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_installation_access_token", Mock(return_value="token"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_pr_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.sort_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_diff_text", Mock(return_value="diff"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.PRDescriptionGenerator.generate_pull_request_desc", Mock(return_value=Mock(desc="generated description")))
    monkeypatch.setattr("github_app.github_helper.pull_requests.patch_pr_body", Mock())

    payload = valid_payload.copy()
    payload["pull_request"]["title"] = ""

    process_pr_desc(payload)

    # Assert that patch_pr_body was called with the expected arguments
    github_app.github_helper.pull_requests.patch_pr_body.assert_called_with(
        "https://api.github.com/repos/owner/repo/pulls/123",
        "generated description",
        1234,
    )

def test_process_pr_desc_no_files_no_description(valid_payload, monkeypatch):
    # Mock dependencies
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_installation_access_token", Mock(return_value="token"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_pr_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.sort_files", Mock(return_value=[]))
    monkeypatch.setattr("github_app.github_helper.pull_requests.get_diff_text", Mock(return_value="diff"))
    monkeypatch.setattr("github_app.github_helper.pull_requests.PRDescriptionGenerator.generate_pull_request_desc", Mock(return_value=Mock(desc="generated description")))
    monkeypatch.setattr("github_app.github_helper.pull_requests.patch_pr_body", Mock())

    payload = valid_payload.copy()
    payload["pull_request"]["body"] = ""

    process_pr_desc(payload)

    # Assert that patch_pr_body was called with the expected arguments
    github_app.github_helper.pull_requests.patch_pr_body.assert_called_with(
        "https://api.github.com/repos/owner/repo/pulls/123",
        "generated description",
        1234,
    )