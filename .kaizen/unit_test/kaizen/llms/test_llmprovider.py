# test_llm_provider.py

import pytest
from unittest.mock import patch, MagicMock
from kaizen.llms.provider import LLMProvider
from kaizen.utils.config import ConfigData
from litellm import Router
import os


@pytest.fixture
def mock_config_data():
    return {
        "language_model": {
            "models": [
                {"model_name": "default", "litellm_params": {"model": "gpt-4o-mini"}}
            ],
            "redis_enabled": False,
            "enable_observability_logging": False,
        }
    }


@pytest.fixture
def mock_litellm():
    with patch("kaizen.llms.provider.litellm") as mock:
        mock.token_counter.return_value = 100
        mock.get_max_tokens.return_value = 4000
        mock.cost_per_token.return_value = (0.01, 0.02)
        yield mock


@pytest.fixture
def llm_provider(mock_config_data, mock_litellm):
    with patch.object(ConfigData, "get_config_data", return_value=mock_config_data):
        return LLMProvider()


def test_initialization(llm_provider):
    assert llm_provider.system_prompt is not None
    assert llm_provider.model_config == {"model": "gpt-4o-mini"}
    assert llm_provider.default_temperature == 0.3


def test_validate_config_correct_setup(llm_provider):
    assert llm_provider.models[0]["model_name"] == "default"


def test_validate_config_missing_language_model():
    with patch.object(ConfigData, "get_config_data", return_value={}):
        with pytest.raises(
            ValueError, match="Missing 'language_model' in configuration"
        ):
            LLMProvider()


def test_token_limit_check_with_valid_prompt(llm_provider, mock_litellm):
    assert llm_provider.is_inside_token_limit("Test prompt") is True


def test_available_tokens_calculation(llm_provider, mock_litellm):
    assert llm_provider.available_tokens("Test message") == 3200


def test_usage_cost_calculation(llm_provider, mock_litellm):
    total_usage = {"prompt_tokens": 100, "completion_tokens": 200}
    cost = llm_provider.get_usage_cost(total_usage)
    assert cost == (0.01, 0.02)


def test_setup_redis_missing_env_vars():
    with patch.dict(os.environ, {}, clear=True):
        with patch.object(
            ConfigData,
            "get_config_data",
            return_value={"language_model": {"redis_enabled": True}},
        ):
            with pytest.raises(
                ValueError,
                match="Redis is enabled but REDIS_HOST or REDIS_PORT environment variables are missing",
            ):
                LLMProvider()


def test_token_limit_check_boundary_condition(llm_provider, mock_litellm):
    mock_litellm.token_counter.return_value = 3200
    assert (
        llm_provider.is_inside_token_limit("Boundary test prompt", percentage=0.8)
        is True
    )
