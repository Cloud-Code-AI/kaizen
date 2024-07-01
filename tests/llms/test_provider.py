import pytest
from unittest.mock import patch
from kaizen.llms.provider import LLMProvider


@pytest.fixture
def mock_config_data():
    with patch("kaizen.utils.config.ConfigData") as MockConfigData:
        mock_config = MockConfigData.return_value
        mock_config.get_config_data.return_value = {
            "language_model": {
                "default_model_config": {"model": "gpt-3.5-turbo-1106"},
                "enable_observability_logging": True,
            }
        }
        yield mock_config


@pytest.fixture
def llm_provider(mock_config_data):
    return LLMProvider()


def test_initialization(llm_provider):
    assert llm_provider.model == "gpt-3.5-turbo-1106"
    assert llm_provider.model_config == {"model": "gpt-3.5-turbo-1106"}


@patch("kaizen.llms.provider.litellm.completion")
def test_chat_completion(mock_completion, llm_provider):
    mock_completion.return_value = {
        "choices": [{"message": {"content": "response"}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 10},
    }
    response, usage = llm_provider.chat_completion("test prompt")
    assert response is not None
    assert usage is not None


@patch("kaizen.llms.provider.litellm.token_counter")
@patch("kaizen.llms.provider.litellm.get_max_tokens")
def test_is_inside_token_limit(mock_get_max_tokens, mock_token_counter, llm_provider):
    mock_token_counter.return_value = 100
    mock_get_max_tokens.return_value = 150

    # Including system prompt in the calculation
    system_prompt_length = len(llm_provider.system_prompt.split())
    user_prompt_length = len("test prompt".split())
    total_length = system_prompt_length + user_prompt_length

    mock_token_counter.return_value = total_length

    assert llm_provider.is_inside_token_limit("test prompt") is True

    mock_token_counter.return_value = 120
    assert llm_provider.is_inside_token_limit("test prompt") is False


@patch("kaizen.llms.provider.litellm.token_counter")
@patch("kaizen.llms.provider.litellm.get_max_tokens")
def test_available_tokens(mock_get_max_tokens, mock_token_counter, llm_provider):
    mock_token_counter.return_value = 100
    mock_get_max_tokens.return_value = 150
    assert llm_provider.available_tokens("test message") == 20


@patch("kaizen.llms.provider.litellm.token_counter")
def test_get_token_count(mock_token_counter, llm_provider):
    mock_token_counter.return_value = 50
    assert llm_provider.get_token_count("test message") == 50
