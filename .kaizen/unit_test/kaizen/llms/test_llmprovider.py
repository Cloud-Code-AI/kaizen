# test_llm_provider.py

import pytest
from unittest.mock import patch, MagicMock
from kaizen.llms.provider import LLMProvider
from kaizen.utils.config import ConfigData
import os

# Fixtures
@pytest.fixture
def mock_config_data():
    return {
        "language_model": {
            "models": [
                {"model_name": "default", "litellm_params": {"model": "gpt-4o-mini"}},
                {"model_name": "embedding", "litellm_params": {"model": "embedding-model"}},
            ],
            "redis_enabled": False,
            "enable_observability_logging": False,
        }
    }

@pytest.fixture
def llm_provider(mock_config_data):
    with patch.object(ConfigData, 'get_config_data', return_value=mock_config_data):
        return LLMProvider()

# Test Cases

def test_validate_config_with_missing_language_model():
    with patch.object(ConfigData, 'get_config_data', return_value={}):
        with pytest.raises(ValueError, match="Missing 'language_model' in configuration"):
            LLMProvider()

def test_setup_provider_initialization(llm_provider):
    assert llm_provider.provider is not None
    assert llm_provider.model == "gpt-4o-mini"

def test_is_inside_token_limit_within_limit(llm_provider):
    with patch('litellm.token_counter', return_value=3200):
        with patch('litellm.get_max_tokens', return_value=4000):
            assert llm_provider.is_inside_token_limit("test prompt")

def test_is_inside_token_limit_exceeds_limit(llm_provider):
    with patch('litellm.token_counter', return_value=3500):
        with patch('litellm.get_max_tokens', return_value=4000):
            assert not llm_provider.is_inside_token_limit("test prompt")

def test_update_usage():
    llm_provider = LLMProvider()
    total_usage = {"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300}
    current_usage = {"prompt_tokens": 50, "completion_tokens": 50, "total_tokens": 100}
    updated_usage = llm_provider.update_usage(total_usage, current_usage)
    assert updated_usage == {"prompt_tokens": 150, "completion_tokens": 250, "total_tokens": 400}

def test_get_token_count(llm_provider):
    with patch('litellm.token_counter', return_value=100):
        assert llm_provider.get_token_count("test message") == 100

def test_setup_redis_with_missing_env_vars(llm_provider):
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Redis is enabled but REDIS_HOST or REDIS_PORT environment variables are missing"):
            llm_provider._setup_redis({})