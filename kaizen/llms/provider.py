import litellm
import os
from typing import Dict, Optional, Any
from kaizen.llms.prompts.general_prompts import BASIC_SYSTEM_PROMPT
from kaizen.utils.config import ConfigData
from litellm import Router
import asyncio
import logging


class LLMProvider:
    DEFAULT_MODEL = "gpt-3.5-turbo-1106"
    DEFAULT_MAX_TOKENS = 4000
    DEFAULT_TEMPERATURE = 0
    DEFAULT_MODEL_CONFIG = {"model": DEFAULT_MODEL}
    DEFAULT_MODEL_NAME = "default"

    def __init__(
        self,
        system_prompt: str = BASIC_SYSTEM_PROMPT,
        model_config: Dict[str, Any] = DEFAULT_MODEL_CONFIG,
        default_temperature: float = 0.3,
    ):
        self.config = ConfigData().get_config_data()
        self.system_prompt = system_prompt
        self.model_config = model_config
        self.default_temperature = default_temperature
        self.logger = logging.getLogger(__name__)

        self._validate_config()
        self._setup_provider()
        self._setup_observability()

    def _validate_config(self) -> None:
        if "language_model" not in self.config:
            raise ValueError("Missing 'language_model' in configuration")

        if "models" in self.config["language_model"]:
            self.models = self.config["language_model"]["models"]
        else:
            self.models = [
                {
                    "model_name": self.DEFAULT_MODEL_NAME,
                    "litellm_params": self.model_config,
                }
            ]

    def _setup_provider(self) -> None:
        provider_kwargs = {
            "model_list": self.models,
            "allowed_fails": 1,
            "enable_pre_call_checks": True,
        }

        if self.config["language_model"].get("redis_enabled", False):
            self._setup_redis(provider_kwargs)

        self.provider = Router(**provider_kwargs)
        self.model = self.models[0]["litellm_params"]["model"]

    def _setup_redis(self, provider_kwargs: Dict[str, Any]) -> None:
        redis_host = os.environ.get("REDIS_HOST")
        redis_port = os.environ.get("REDIS_PORT")
        if not redis_host or not redis_port:
            raise ValueError(
                "Redis is enabled but REDIS_HOST or REDIS_PORT environment variables are missing"
            )

        provider_kwargs.update(
            {
                "redis_host": redis_host,
                "redis_port": redis_port,
                "routing_strategy": "usage-based-routing-v2",
            }
        )

    def _setup_observability(self) -> None:
        if self.config["language_model"].get("enable_observability_logging", False):
            litellm.success_callback = ["supabase"]
            litellm.failure_callback = ["supabase"]

    async def router_acompletion(self, messages, user, custom_model):
        response = await self.provider.acompletion(
            messages=messages, user=user, **custom_model
        )
        return response

    def chat_completion(
        self,
        prompt,
        user: str = None,
        model="default",
        custom_model=None,
        messages=None,
    ):
        if not messages:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ]
        if not custom_model:
            custom_model = {"model": "default"}
        if "temperature" not in custom_model:
            custom_model["temperature"] = self.default_temperature

        # TODO: Add better way to manage this async calls
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(
            self.router_acompletion(messages, user, custom_model)
        )
        return response["choices"][0]["message"]["content"], response["usage"]

    def is_inside_token_limit(self, PROMPT: str, percentage: float = 0.8) -> bool:
        # TODO: Also include system prompt
        messages = [{"user": "role", "content": PROMPT}]
        token_count = litellm.token_counter(model=self.model, messages=messages)
        max_tokens = litellm.get_max_tokens(self.model)
        return token_count <= max_tokens * percentage

    def available_tokens(self, message: str, percentage: float = 0.8) -> int:
        max_tokens = litellm.get_max_tokens(self.model)
        used_tokens = litellm.token_counter(model=self.model, text=message)
        return int(max_tokens * percentage) - used_tokens

    def get_token_count(self, message: str) -> int:
        return litellm.token_counter(model=self.model, text=message)

    def update_usage(
        self, total_usage: Optional[Dict[str, int]], current_usage: Dict[str, int]
    ) -> Dict[str, int]:
        if total_usage is not None:
            return {key: total_usage[key] + current_usage[key] for key in total_usage}
        return {key: current_usage[key] for key in current_usage}

    def get_usage_cost(self, total_usage: Dict[str, int]) -> float:
        return litellm.cost_per_token(
            self.model, total_usage["prompt_tokens"], total_usage["completion_tokens"]
        )
