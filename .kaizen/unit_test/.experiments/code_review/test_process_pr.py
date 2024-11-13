import pytest
from unittest.mock import patch, MagicMock
from kaizen.reviewer.code_review import CodeReviewer
from kaizen.llms.provider import LLMProvider
from kaizen.formatters.code_review_formatter import create_pr_review_text
from github_app.github_helper.utils import get_diff_text, get_pr_files
from github_app.github_helper.pull_requests import create_review_comments
from .experiments.code_review.main import process_pr

@pytest.fixture
def mock_dependencies():
    with patch('kaizen.reviewer.code_review.CodeReviewer') as mock_reviewer, \
         patch('kaizen.llms.provider.LLMProvider') as mock_llm_provider, \
         patch('github_app.github_helper.utils.get_diff_text') as mock_get_diff_text, \
         patch('github_app.github_helper.utils.get_pr_files') as mock_get_pr_files, \
         patch('github_app.github_helper.pull_requests.create_review_comments') as mock_create_review_comments, \
         patch('kaizen.formatters.code_review_formatter.create_pr_review_text') as mock_create_pr_review_text:
        
        yield {
            'reviewer': mock_reviewer,
            'llm_provider': mock_llm_provider,
            'get_diff_text': mock_get_diff_text,
            'get_pr_files': mock_get_pr_files,
            'create_review_comments': mock_create_review_comments,
            'create_pr_review_text': mock_create_pr_review_text
        }

def test_process_pr_normal_case(mock_dependencies):
    # Arrange
    pr_url = "https://github.com/org/repo/pull/123"
    mock_diff_text = "Sample diff text"
    mock_pr_files = [{"filename": "file1.py", "patch": "Sample patch"}]
    mock_review_data = MagicMock(
        topics={"important": ["Topic 1", "Topic 2"]},
        code_quality="Good",
        model_name="gpt-4",
        usage={"prompt_tokens": 100, "completion_tokens": 50},
        issues=["Issue 1", "Issue 2"]
    )
    
    mock_dependencies['get_diff_text'].return_value = mock_diff_text
    mock_dependencies['get_pr_files'].return_value = mock_pr_files
    mock_dependencies['reviewer'].return_value.review_pull_request.return_value = mock_review_data
    mock_dependencies['create_review_comments'].return_value = (["Comment 1"], ["Topic 1", "Topic 2"])
    mock_dependencies['create_pr_review_text'].return_value = "Sample review text"

    # Act
    review_desc, comments, issues, combined_diff_data = process_pr(pr_url)

    # Assert
    assert "PR URL: https://github.com/org/repo/pull/123" in review_desc
    assert "Sample review text" in review_desc
    assert "Cost Usage (gpt-4)" in review_desc
    assert comments == ["Comment 1"]
    assert issues == ["Issue 1", "Issue 2"]
    assert "File Name: file1.py" in combined_diff_data
    assert "Patch Details: Sample patch" in combined_diff_data

def test_process_pr_empty_files(mock_dependencies):
    # Arrange
    pr_url = "https://github.com/org/repo/pull/124"
    mock_diff_text = "Sample diff text"
    mock_pr_files = []
    mock_review_data = MagicMock(
        topics={},
        code_quality="N/A",
        model_name="gpt-3.5-turbo",
        usage={"prompt_tokens": 50, "completion_tokens": 25},
        issues=[]
    )
    
    mock_dependencies['get_diff_text'].return_value = mock_diff_text
    mock_dependencies['get_pr_files'].return_value = mock_pr_files
    mock_dependencies['reviewer'].return_value.review_pull_request.return_value = mock_review_data
    mock_dependencies['create_review_comments'].return_value = ([], [])
    mock_dependencies['create_pr_review_text'].return_value = "No changes found"

    # Act
    review_desc, comments, issues, combined_diff_data = process_pr(pr_url)

    # Assert
    assert "PR URL: https://github.com/org/repo/pull/124" in review_desc
    assert "No changes found" in review_desc
    assert "Cost Usage (gpt-3.5-turbo)" in review_desc
    assert comments == []
    assert issues == []
    assert combined_diff_data == ""

@pytest.mark.parametrize("exception_class", [ValueError, ConnectionError, Exception])
def test_process_pr_invalid_url(mock_dependencies, exception_class):
    # Arrange
    pr_url = "https://invalid-url.com/pr/123"
    mock_dependencies['get_diff_text'].side_effect = exception_class("Error fetching diff")

    # Act & Assert
    with pytest.raises(exception_class):
        process_pr(pr_url)

    # Verify that the function attempts to get the diff text
    mock_dependencies['get_diff_text'].assert_called_once()
    # Verify that no further processing occurs after the exception
    mock_dependencies['get_pr_files'].assert_not_called()
    mock_dependencies['reviewer'].return_value.review_pull_request.assert_not_called()