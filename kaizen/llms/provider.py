import litellm
import os
from kaizen.llms.prompts.general_prompts import BASIC_SYSTEM_PROMPT
from kaizen.utils.config import ConfigData
from litellm import Router
import asyncio

class LLMProvider:
    DEFAULT_MODEL = "gpt-3.5-turbo-1106"
    DEFAULT_MAX_TOKENS = 4000
    DEFAULT_TEMPERATURE = 0
    DEFAULT_MODEL_CONFIG = {"model": DEFAULT_MODEL}

    def __init__(
        self,
        system_prompt=BASIC_SYSTEM_PROMPT,
        model_config=DEFAULT_MODEL_CONFIG,
        default_temperature=0.3,
    ):
        self.config = ConfigData().get_config_data()
        self.system_prompt = system_prompt
        self.model_config = model_config
        self.default_temperature = default_temperature

        if "models" in self.config.get("language_model"):
            self.models = self.config["language_model"]["models"]
        else:
            self.models = [
                {"model_name": "default", "litellm_params": self.model_config}
            ]

        if self.config.get("language_model", {}).get("redis_enabled", False):
            # TODO: Add check for redis server creds if redis enabled
            self.provider = Router(
                model_list=self.models,
                redis_host=os.environ["REDIS_HOST"],
                redis_port=os.environ["REDIS_PORT"],
                routing_strategy="usage-based-routing-v2",
                allowed_fails=1,
            )
        else:
            self.provider = Router(model_list=self.models, allowed_fails=1)

        self.model = self.model_config["model"]
        if self.config.get("language_model", {}).get(
            "enable_observability_logging", False
        ):
            # set callbacks
            litellm.success_callback = ["supabase"]
            litellm.failure_callback = ["supabase"]
    
    async def router_acompletion(self, messages, user, custom_model):
        response = await self.provider.acompletion(
            messages=messages,
            user=user,
            **custom_model
        )
        print(response)
        return response

    def chat_completion(
        self, prompt, user: str = None, model="default", custom_model=None, messages=None
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

        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(self.router_acompletion(messages, user, custom_model))
        return response["choices"][0]["message"]["content"], response["usage"]

    def is_inside_token_limit(self, PROMPT, percentage=0.8):
        # TODO: Also include system prompt
        messages = [{"user": "role", "content": PROMPT}]
        if (
            litellm.token_counter(model=self.model, messages=messages)
            > litellm.get_max_tokens(self.model) * percentage
        ):
            return False
        return True

    def available_tokens(self, message, percentage=0.8):
        """
        Calculate the number of tokens available for a single request after accounting for the tokens consumed by the prompt.

        Args:
            message (str): The input message for which tokens are being calculated.
            percentage (float, optional): The percentage of total tokens to be considered available. Defaults to 0.8.

        Returns:
            int: The number of tokens available for a single request.
        """
        return litellm.get_max_tokens(self.model) * percentage - litellm.token_counter(
            model=self.model, text=message
        )

    def get_token_count(self, message):
        return litellm.token_counter(model=self.model, text=message)

    def update_usage(self, total_usage, current_usage):
        """
        Update the total usage with the current usage values.

        This function updates the `total_usage` dictionary by adding the values from the
        `current_usage` dictionary. If `total_usage` is None, it initializes `total_usage` with
        the values from `current_usage`.

        Args:
            total_usage (dict or None): The dictionary containing the cumulative usage information.
                If None, it will be initialized with the values from `current_usage`.
            current_usage (dict): A dictionary containing the current usage information with keys
                corresponding to those in `total_usage`.

        Returns:
            dict: The updated total usage dictionary with the values from `current_usage` added
            to the corresponding keys in `total_usage`.

        Example:
            total_usage = {
                "prompt_tokens": 150,
                "completion_tokens": 250
            }
            current_usage = {
                "prompt_tokens": 100,
                "completion_tokens": 200
            }
            updated_usage = instance.update_usage(total_usage, current_usage)
            print(updated_usage)
            # Output: {"prompt_tokens": 250, "completion_tokens": 450}

            # If total_usage is None
            total_usage = None
            updated_usage = instance.update_usage(total_usage, current_usage)
            print(updated_usage)
            # Output: {"prompt_tokens": 100, "completion_tokens": 200}
        """

        if total_usage is not None:
            total_usage = {
                key: total_usage[key] + current_usage[key] for key in total_usage
            }
        else:
            total_usage = {key[0]: current_usage[key[0]] for key in current_usage}
        return total_usage

    def get_usage_cost(self, total_usage):
        """
        Calculate the cost of usage based on the number of tokens used in the prompt and completion.

        Args:
            total_usage (dict): A dictionary containing the usage information with the following keys:
                - "prompt_tokens" (int): The number of tokens used in the prompt.
                - "completion_tokens" (int): The number of tokens used in the completion.

        Returns:
            float: The total cost of the usage based on the model's cost per token.

        Example:
            total_usage = {
                "prompt_tokens": 100,
                "completion_tokens": 200
            }
            cost = instance.get_usage_cost(total_usage)
            print(cost)  # Output will depend on the model's cost per token.
        """
        return litellm.cost_per_token(
            self.model, total_usage["prompt_tokens"], total_usage["completion_tokens"]
        )
