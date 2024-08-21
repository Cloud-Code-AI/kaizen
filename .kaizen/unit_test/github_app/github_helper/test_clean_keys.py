import pytest
from /tmp/tmpn_ihnj4m/github_app/github_helper.pull_requests import clean_keys, confidence_mapping

@pytest.fixture
def sample_topics():
    return {
        "Topic1": [
            {"confidence": "high", "comment": "Great feature"},
            {"confidence": "medium", "comment": "Needs improvement"}
        ],
        "Topic2": [
            {"confidence": "low", "comment": "Not useful"}
        ]
    }

def test_typical_input(sample_topics):
    result = clean_keys(sample_topics)
    assert isinstance(result, dict)
    assert len(result) == 2
    assert "Topic1" in result and "Topic2" in result
    assert len(result["Topic1"]) == 2
    assert len(result["Topic2"]) == 1

@pytest.mark.parametrize("min_confidence,expected_count", [
    ("low", 3),
    ("medium", 2),
    ("high", 1)
])
def test_min_confidence(sample_topics, min_confidence, expected_count):
    result = clean_keys(sample_topics, min_confidence)
    assert sum(len(reviews) for reviews in result.values()) == expected_count

def test_reasoning_field(sample_topics):
    result = clean_keys(sample_topics)
    for topic, reviews in result.items():
        for review in reviews:
            assert "reasoning" in review
            assert review["reasoning"] == review["comment"]

def test_empty_input():
    result = clean_keys({})
    assert result == {}

def test_single_topic_single_review():
    input_data = {"Topic": [{"confidence": "medium", "comment": "Test"}]}
    result = clean_keys(input_data)
    assert len(result) == 1
    assert len(result["Topic"]) == 1
    assert result["Topic"][0]["reasoning"] == "Test"

def test_large_input():
    large_input = {f"Topic{i}": [{"confidence": "medium", "comment": f"Comment{j}"} for j in range(100)] for i in range(100)}
    result = clean_keys(large_input)
    assert len(result) == 100
    assert all(len(reviews) == 100 for reviews in result.values())

def test_invalid_confidence(sample_topics):
    sample_topics["Topic3"] = [{"confidence": "invalid", "comment": "Test"}]
    with pytest.raises(KeyError):
        clean_keys(sample_topics)

def test_missing_confidence(sample_topics):
    sample_topics["Topic3"] = [{"comment": "Test"}]
    with pytest.raises(KeyError):
        clean_keys(sample_topics)

def test_non_existent_min_confidence(sample_topics):
    with pytest.raises(Exception):
        clean_keys(sample_topics, "non_existent")

def test_min_confidence_lowest(sample_topics):
    result = clean_keys(sample_topics, "low")
    assert sum(len(reviews) for reviews in result.values()) == 3

def test_min_confidence_highest(sample_topics):
    result = clean_keys(sample_topics, "high")
    assert sum(len(reviews) for reviews in result.values()) == 1

def test_empty_comment():
    input_data = {"Topic": [{"confidence": "medium", "comment": ""}]}
    result = clean_keys(input_data)
    assert result["Topic"][0]["reasoning"] == ""

# Additional test to check if the function returns a new dictionary
def test_return_new_dictionary(sample_topics):
    result = clean_keys(sample_topics)
    assert result is not sample_topics

# Test to check if the issues variable is correctly populated
def test_issues_population(sample_topics):
    clean_keys(sample_topics)
    # Note: We can't directly access the 'issues' variable as it's local to the function.
    # We would need to modify the function to return this value for testing.
    # For now, we can only check if it doesn't raise an exception.

if __name__ == "__main__":
    pytest.main()