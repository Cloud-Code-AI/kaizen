import litellm
import os
from typing import Dict, Optional, Any
from kaizen.llms.prompts.general_prompts import BASIC_SYSTEM_PROMPT
from kaizen.utils.config import ConfigData
from kaizen.helpers.general import retry
from kaizen.helpers.parser import extract_json
from litellm import Router
import logging
from collections import defaultdict

DEFAULT_MAX_TOKENS = 8000


def set_all_loggers_to_ERROR():
    # print("All Loggers and their levels:")
    for name, logger in logging.Logger.manager.loggerDict.items():
        if isinstance(logger, logging.Logger):
            # print(f"Logger: {name}, Level: {logging.getLevelName(logger.level)}")
            logging.getLogger(name).setLevel(logging.ERROR)
        else:
            # print(f"PlaceHolder: {name}")
            pass


set_all_loggers_to_ERROR()

# Set litellm log level to ERROR
logging.getLogger("LiteLLM").setLevel(logging.ERROR)
logging.getLogger("LiteLLM Router").setLevel(logging.ERROR)
logging.getLogger("LiteLLM Proxy").setLevel(logging.ERROR)
LOGLEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOGLEVEL, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class LLMProvider:
    DEFAULT_MODEL = "gpt-3.5-turbo-1106"
    DEFAULT_MAX_TOKENS = 4000
    DEFAULT_TEMPERATURE = 0
    DEFAULT_MODEL_CONFIG = {"model": DEFAULT_MODEL}
    DEFAULT_MODEL_NAME = "default"
    DEFAULT_USAGE = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    def __init__(
        self,
        system_prompt: str = BASIC_SYSTEM_PROMPT,
        model_config: Dict[str, Any] = DEFAULT_MODEL_CONFIG,
        default_temperature: float = 0.3,
        callback_obj="supabase",
    ):
        self.config = ConfigData().get_config_data()
        self.system_prompt = system_prompt
        self.model_config = model_config
        self.default_temperature = default_temperature
        self.callback_obj = "supabase"
        self.logger = logging.getLogger(
            __name__,
        )

        self._validate_config()
        self._setup_provider()
        self._setup_observability()
        self._register_unkown_models()

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
            "routing_strategy": "simple-shuffle",
        }

        if self.config["language_model"].get("redis_enabled", False):
            self._setup_redis(provider_kwargs)

        self.provider = Router(**provider_kwargs)
        self.model = self.models[0]["litellm_params"]["model"]
        self.model_group_to_name = dict(
            defaultdict(
                list,
                {
                    item["model_name"]: [
                        i["litellm_params"]["model"]
                        for i in self.models
                        if i["model_name"] == item["model_name"]
                    ]
                    for item in self.models
                },
            )
        )

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
            litellm.success_callback = [self.callback_obj]
            litellm.failure_callback = [self.callback_obj]

    def _register_unkown_models(self) -> None:
        for model_data in self.models:
            model_info = model_data.get("model_info", {})
            if "litellm_provider" in model_info:
                # Register this model
                litellm.register_model({model_data["model_name"]: model_info})

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
            custom_model = {"model": model}
        if "temperature" not in custom_model:
            custom_model["temperature"] = self.default_temperature

        response = self.provider.completion(
            messages=messages, user=user, **custom_model
        )
        self.model = response["model"]
        return response["choices"][0]["message"]["content"], response["usage"]

    def raw_chat_completion(
        self,
        prompt,
        user: str = None,
        model="default",
        custom_model=None,
        messages=None,
        n_choices=1,
    ):
        custom_model["n"] = n_choices
        if not messages:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt},
            ]
        if not custom_model:
            custom_model = {"model": model}
        if "temperature" not in custom_model:
            custom_model["temperature"] = self.default_temperature

        response = self.provider.completion(
            messages=messages, user=user, **custom_model
        )
        self.model = response["model"]
        return response, response["usage"]

    @retry(max_attempts=3, delay=1)
    def chat_completion_with_json(
        self,
        prompt,
        user: str = None,
        model="default",
        custom_model=None,
        messages=None,
    ):
        response, usage = self.chat_completion(
            prompt=prompt,
            user=user,
            model=model,
            custom_model=custom_model,
            messages=messages,
        )
        response = extract_json(response)
        return response, usage

    @retry(max_attempts=3, delay=1)
    def chat_completion_with_retry(
        self,
        prompt,
        user: str = None,
        model="default",
        custom_model=None,
        messages=None,
    ):
        response, usage = self.chat_completion(
            prompt=prompt,
            user=user,
            model=model,
            custom_model=custom_model,
            messages=messages,
        )
        return response, usage

    def is_inside_token_limit(self, PROMPT: str, percentage: float = 0.8) -> bool:
        # Include system prompt in token calculation
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": PROMPT},
        ]
        token_count = litellm.token_counter(model=self.model, messages=messages)
        max_tokens = litellm.get_max_tokens(self.model)
        if not max_tokens:
            max_tokens = DEFAULT_MAX_TOKENS
        return token_count <= max_tokens * percentage

    def available_tokens(
        self, message: str, percentage: float = 0.8, model: str = None
    ) -> int:
        if not model:
            model = self.model
        max_tokens = litellm.get_max_tokens(model)
        used_tokens = litellm.token_counter(model=model, text=message)
        if max_tokens:
            return int(max_tokens * percentage) - used_tokens
        else:
            return DEFAULT_MAX_TOKENS - used_tokens

    def get_token_count(self, message: str, model: str = None) -> int:
        if not model:
            model = self.model
        return litellm.token_counter(model=model, text=message)

    def update_usage(
        self, total_usage: Optional[Dict[str, int]], current_usage: Dict[str, int]
    ) -> Dict[str, int]:
        if total_usage is not None:
            return {key: total_usage[key] + current_usage[key] for key in total_usage}
        return {key: current_usage[key] for key in current_usage}

    def get_usage_cost(self, total_usage: Dict[str, int], model: str = None) -> float:
        if not model:
            model = self.model
        try:
            return litellm.cost_per_token(
                model, total_usage["prompt_tokens"], total_usage["completion_tokens"]
            )
        except Exception:
            return 0, 0

    def get_text_embedding(self, text):
        # for model in self.config["language_model"]["models"]:
        #     if model["model_name"] == "embedding":
        #         break
        response = self.provider.embedding(
            model="embedding", input=[text], dimensions=1536, encoding_format="float"
        )
        return response["data"], response["usage"]
