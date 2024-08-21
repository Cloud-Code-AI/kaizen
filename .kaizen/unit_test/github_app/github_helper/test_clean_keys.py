import pytest
from /tmp/tmprfhk8pt0.github_app.github_helper.pull_requests import clean_keys, confidence_mapping

@pytest.fixture
def sample_topics():
    return {
        "Topic1": [
            {"confidence": "high", "comment": "Good comment", "reasoning": "Valid reason"},
            {"confidence": "medium", "comment": "Average comment"},
        ],
        "Topic2": [
            {"confidence": "low", "comment": "Poor comment"},
        ]
    }

def test_normal_case_no_min_confidence(sample_topics):
    result = clean_keys(sample_topics)
    assert len(result) == 2
    assert len(result["Topic1"]) == 2
    assert len(result["Topic2"]) == 1
    assert result["Topic1"][1]["reasoning"] == "Average comment"

def test_normal_case_with_min_confidence(sample_topics):
    result = clean_keys(sample_topics, min_confidence="medium")
    assert len(result) == 2
    assert len(result["Topic1"]) == 2
    assert len(result["Topic2"]) == 0

def test_edge_case_empty_topics():
    result = clean_keys({})
    assert result == {}

def test_edge_case_no_reviews():
    topics = {"Topic1": [], "Topic2": []}
    result = clean_keys(topics)
    assert result == {"Topic1": [], "Topic2": []}

def test_error_handling_invalid_confidence(capsys):
    topics = {"Topic1": [{"confidence": "invalid", "comment": "Test"}]}
    clean_keys(topics, min_confidence="invalid")
    captured = capsys.readouterr()
    assert "Error" in captured.out

@pytest.mark.parametrize("min_confidence, expected_count", [
    ("low", 3),
    ("medium", 2),
    ("high", 1)
])
def test_boundary_condition_min_confidence(sample_topics, min_confidence, expected_count):
    result = clean_keys(sample_topics, min_confidence=min_confidence)
    total_reviews = sum(len(reviews) for reviews in result.values())
    assert total_reviews == expected_count

def test_reasoning_added_when_missing(sample_topics):
    result = clean_keys(sample_topics)
    assert result["Topic1"][1]["reasoning"] == "Average comment"
    assert result["Topic2"][0]["reasoning"] == "Poor comment"

def test_issues_variable(sample_topics, capsys):
    clean_keys(sample_topics)
    captured = capsys.readouterr()
    assert "issues:" in captured.out
    assert "confidence" in captured.out
    assert "comment" in captured.out