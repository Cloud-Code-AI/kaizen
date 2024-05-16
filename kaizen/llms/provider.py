import litellm
from kaizen.llms.prompts import BASIC_SYSTEM_PROMPT
from kaizen.utils.config import CONFIG_DATA


class LLMProvider:
    DEFAULT_MODEL = "gpt-3.5-turbo-1106"
    DEFAULT_MAX_TOKENS = 1000
    DEFAULT_TEMPERATURE = 0

    def __init__(
        self,
        system_prompt=BASIC_SYSTEM_PROMPT,
        model=DEFAULT_MODEL,
        max_tokens=DEFAULT_MAX_TOKENS,
        temperature=DEFAULT_TEMPERATURE,
    ):
        self.system_prompt = system_prompt
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        if CONFIG_DATA.get("language_model", {}).get(
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
        response = litellm.completion(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            user=user,
        )
        return response["choices"][0]["message"]["content"], response["usage"]

    def is_inside_token_limit(self, PROMPT, percentage=0.7):
        messages = [{"user": "role", "content": PROMPT}]
        if (
            litellm.token_counter(model=self.model, messages=messages)
            > litellm.get_max_tokens(self.model) * percentage
        ):
            return False
        return True

    def available_tokens(self, message, percentage=0.8):
        return litellm.get_max_tokens(self.model) * percentage - litellm.token_counter(
            self.model, message
        )

    def get_token_count(self, message):
        return litellm.token_counter(self.model, message)

    def update_usage(self, total_usage, current_usage):
        if total_usage is not None:
            total_usage = {
                key: total_usage[key] + current_usage[key] for key in total_usage
            }
        else:
            total_usage = current_usage
        return total_usage

    def get_usage_cost(self, total_usage):
        return litellm.cost_per_token(
            self.model, total_usage["prompt_tokens"], total_usage["completion_tokens"]
        )
