import litellm
from kaizen.llms.prompts import BASIC_SYSTEM_PROMPT
from kaizen.utils.config import ConfigData


class LLMProvider:
    DEFAULT_MODEL = "gpt-3.5-turbo-1106"
    DEFAULT_MAX_TOKENS = 4000
    DEFAULT_TEMPERATURE = 0
    DEFAULT_MODEL_CONFIG = {"model": DEFAULT_MODEL}

    def __init__(
        self, system_prompt=BASIC_SYSTEM_PROMPT, model_config=DEFAULT_MODEL_CONFIG
    ):
        self.config = ConfigData().get_config_data()
        self.system_prompt = system_prompt
        self.model_config = model_config
        if "default_model_config" in self.config.get("language_model", {}):
            self.model_config = self.config["language_model"]["default_model_config"]
        self.model = self.model_config["model"]
        if self.config.get("language_model", {}).get(
            "enable_observability_logging", False
        ):
            # set callbacks
            litellm.success_callback = ["supabase"]
            litellm.failure_callback = ["supabase"]

    def chat_completion(self, prompt, user: str = None):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]

        response = litellm.completion(messages=messages, user=user, **self.model_config)
        return response["choices"][0]["message"]["content"], response["usage"]

    def is_inside_token_limit(self, PROMPT, percentage=0.7):
        # TODO: Also include system prompt
        messages = [{"user": "role", "content": PROMPT}]
        if (
            litellm.token_counter(model=self.model, messages=messages)
            > litellm.get_max_tokens(self.model) * percentage
        ):
            return False
        return True

    def available_tokens(self, message, percentage=0.8):
        return litellm.get_max_tokens(self.model) * percentage - litellm.token_counter(
            model=self.model, text=message
        )

    def get_token_count(self, message):
        return litellm.token_counter(model=self.model, text=message)

    def update_usage(self, total_usage, current_usage):
        if total_usage is not None:
            total_usage = {
                key: total_usage[key] + current_usage[key] for key in total_usage
            }
        else:
            total_usage = {key[0]: current_usage[key[0]] for key in current_usage}
        return total_usage

    def get_usage_cost(self, total_usage):
        return litellm.cost_per_token(
            self.model, total_usage["prompt_tokens"], total_usage["completion_tokens"]
        )
