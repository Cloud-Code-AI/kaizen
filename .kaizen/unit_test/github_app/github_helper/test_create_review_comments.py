import pytest

# Assuming the function is located at /tmp/tmpn_ihnj4m/github_app/github_helper/pull_requests.py
from /tmp/tmpn_ihnj4m/github_app/github_helper.pull_requests import create_review_comments

# Mock confidence mapping for testing purposes
confidence_mapping = {
    "low": 1,
    "medium": 3,
    "high": 5
}

@pytest.fixture
def setup_confidence_mapping(monkeypatch):
    monkeypatch.setattr("/tmp/tmpn_ihnj4m/github_app/github_helper.pull_requests", "confidence_mapping", confidence_mapping)

def test_normal_case_single_topic(setup_confidence_mapping):
    topics = {
        "topic1": [{"confidence": "high", "comment": "Great work!"}]
    }
    expected_comments = [{"confidence": "high", "comment": "Great work!"}]
    comments, returned_topics = create_review_comments(topics, confidence_level=4)
    assert comments == expected_comments
    assert returned_topics == topics

def test_normal_case_multiple_topics(setup_confidence_mapping):
    topics = {
        "topic1": [{"confidence": "high", "comment": "Great work!"}],
        "topic2": [{"confidence": "medium", "comment": "Needs improvement."}]
    }
    expected_comments = [{"confidence": "high", "comment": "Great work!"}]
    comments, returned_topics = create_review_comments(topics, confidence_level=4)
    assert comments == expected_comments
    assert returned_topics == topics

def test_edge_case_empty_topics(setup_confidence_mapping):
    topics = {}
    expected_comments = []
    comments, returned_topics = create_review_comments(topics, confidence_level=4)
    assert comments == expected_comments
    assert returned_topics == topics

def test_edge_case_no_reviews(setup_confidence_mapping):
    topics = {
        "topic1": []
    }
    expected_comments = []
    comments, returned_topics = create_review_comments(topics, confidence_level=4)
    assert comments == expected_comments
    assert returned_topics == topics

def test_error_handling_invalid_confidence_level(setup_confidence_mapping):
    topics = {
        "topic1": [{"confidence": "high", "comment": "Great work!"}]
    }
    with pytest.raises(KeyError):
        create_review_comments(topics, confidence_level="invalid")

@pytest.mark.parametrize("confidence_level, expected_comments", [
    (1, [{"confidence": "high", "comment": "Great work!"}, {"confidence": "medium", "comment": "Needs improvement."}]),
    (3, [{"confidence": "high", "comment": "Great work!"}]),
    (5, [])
])
def test_boundary_condition_confidence_level(setup_confidence_mapping, confidence_level, expected_comments):
    topics = {
        "topic1": [{"confidence": "high", "comment": "Great work!"}],
        "topic2": [{"confidence": "medium", "comment": "Needs improvement."}]
    }
    comments, returned_topics = create_review_comments(topics, confidence_level=confidence_level)
    assert comments == expected_comments
    assert returned_topics == topics