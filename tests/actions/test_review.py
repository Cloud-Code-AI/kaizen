import pytest
import json
from kaizen.reviewer.code_review import CodeReviewer
from unittest.mock import Mock
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.code_review_prompts import CODE_REVIEW_PROMPT

with open("tests/data/actions/valid_review.json") as f:
    data = json.load(f)


# @pytest.mark.parametrize("valid_review", data)
# def test_review_pull_request(valid_review):
#     # Act
#     code_reviewer = CodeReviewer()
#     result = code_reviewer.review_pull_request(
#         valid_review["input"]["diff"],
#         valid_review["input"]["title"],
#         valid_review["input"]["description"],
#         pull_request_files=[],
#         user="pytest",
#     )
#     review = code_reviewer.create_pr_review_text(result.topics)

#     assert fuzz.ratio(review, valid_review["output"]) > 95


@pytest.fixture
def code_reviewer():
    code_reviewer = CodeReviewer()
    mock_provider = Mock(spec=LLMProvider)
    code_reviewer.provider = mock_provider
    return code_reviewer


def test_is_code_review_prompt_within_limit_true(code_reviewer):
    diff_text = "sample diff text"
    pull_request_title = "Sample Pull Request Title"
    pull_request_desc = "Sample Pull Request Description"
    prompt = CODE_REVIEW_PROMPT.format(
        PULL_REQUEST_TITLE=pull_request_title,
        PULL_REQUEST_DESC=pull_request_desc,
        CODE_DIFF=diff_text,
    )
    code_reviewer.provider.is_inside_token_limit.return_value = True

    result = code_reviewer.is_code_review_prompt_within_limit(
        diff_text, pull_request_title, pull_request_desc
    )

    assert result
    code_reviewer.provider.is_inside_token_limit.assert_called_once_with(PROMPT=prompt)


def test_is_code_review_prompt_within_limit_false(code_reviewer):
    diff_text = "very long diff text" * 1000
    pull_request_title = "Sample Pull Request Title"
    pull_request_desc = "Sample Pull Request Description"
    prompt = CODE_REVIEW_PROMPT.format(
        PULL_REQUEST_TITLE=pull_request_title,
        PULL_REQUEST_DESC=pull_request_desc,
        CODE_DIFF=diff_text,
    )
    code_reviewer.provider.is_inside_token_limit.return_value = False

    result = code_reviewer.is_code_review_prompt_within_limit(
        diff_text, pull_request_title, pull_request_desc
    )

    assert not result
    code_reviewer.provider.is_inside_token_limit.assert_called_once_with(PROMPT=prompt)
