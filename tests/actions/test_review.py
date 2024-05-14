import pytest
import json
from kaizen.reviewer.code_review import CodeReviewer
from fuzzywuzzy import fuzz

with open("tests/data/actions/valid_review.json") as f:
    data = json.load(f)


@pytest.mark.parametrize("valid_review", data)
def test_review_pull_request(valid_review):
    # Act
    code_reviewer = CodeReviewer()
    result = code_reviewer.review_pull_request(
        valid_review["input"]["diff"],
        valid_review["input"]["title"],
        valid_review["input"]["description"],
        pull_request_files=[],
        user="pytest",
    )

    assert fuzz.ratio(result, valid_review["output"]) > 95
