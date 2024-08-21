import pytest
from pull_requests import create_review_comments, confidence_mapping

# Test data
topics = {
    "topic1": [
        {"confidence": 5, "comment": "High confidence review 1"},
        {"confidence": 3, "comment": "Low confidence review 1"},
        {"confidence": 4, "comment": "Medium confidence review 1"},
    ],
    "topic2": [
        {"confidence": 2, "comment": "Low confidence review 2"},
        {"confidence": 5, "comment": "High confidence review 2"},
    ],
}

# Fixtures
@pytest.fixture
def empty_topics():
    return {}

@pytest.fixture
def single_topic_single_review():
    return {"topic1": [{"confidence": 4, "comment": "Medium confidence review"}]}

@pytest.fixture
def all_low_confidence_reviews():
    return {
        "topic1": [
            {"confidence": 2, "comment": "Low confidence review 1"},
            {"confidence": 1, "comment": "Low confidence review 2"},
        ]
    }

@pytest.fixture
def invalid_confidence_level_reviews():
    return {
        "topic1": [
            {"confidence": "high", "comment": "Invalid confidence level review"},
            {"confidence": 4, "comment": "Valid confidence review"},
        ]
    }

@pytest.fixture
def missing_confidence_key_reviews():
    return {
        "topic1": [
            {"comment": "Missing confidence key review"},
            {"confidence": 4, "comment": "Valid confidence review"},
        ]
    }

# Test cases
def test_create_review_comments_default_confidence_level(topics):
    comments, _ = create_review_comments(topics)
    assert len(comments) == 3
    assert all(confidence_mapping[review["confidence"]] > 4 for review in comments)

def test_create_review_comments_custom_confidence_level(topics):
    comments, _ = create_review_comments(topics, confidence_level=3)
    assert len(comments) == 4
    assert all(confidence_mapping[review["confidence"]] > 3 for review in comments)

def test_create_review_comments_empty_topics(empty_topics):
    comments, topics = create_review_comments(empty_topics)
    assert len(comments) == 0
    assert topics == {}

def test_create_review_comments_all_low_confidence_reviews(all_low_confidence_reviews):
    comments, _ = create_review_comments(all_low_confidence_reviews)
    assert len(comments) == 0

def test_create_review_comments_single_topic_single_review(single_topic_single_review):
    comments, _ = create_review_comments(single_topic_single_review)
    assert len(comments) == 1
    assert comments[0]["confidence"] == 4

def test_create_review_comments_invalid_confidence_level_reviews(invalid_confidence_level_reviews):
    comments, _ = create_review_comments(invalid_confidence_level_reviews)
    assert len(comments) == 1
    assert comments[0]["confidence"] == 4

def test_create_review_comments_missing_confidence_key_reviews(missing_confidence_key_reviews):
    comments, _ = create_review_comments(missing_confidence_key_reviews)
    assert len(comments) == 1
    assert comments[0]["confidence"] == 4

@pytest.mark.parametrize("confidence_level", [0, 4, 5])
def test_create_review_comments_boundary_confidence_levels(confidence_level, topics):
    comments, _ = create_review_comments(topics, confidence_level=confidence_level)
    expected_count = sum(
        1 for _, reviews in topics.items() for review in reviews if confidence_mapping[review["confidence"]] > confidence_level
    )
    assert len(comments) == expected_count

def test_create_review_comments_invalid_confidence_level_parameter():
    with pytest.raises(ValueError):
        create_review_comments(topics, confidence_level="invalid")