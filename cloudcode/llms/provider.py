from litellm import completion
from cloudcode.llms.prompts import BASIC_SYSTEM_PROMPT


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

    def chat_completion(self, prompt):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt},
        ]
        response = completion(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response["choices"][0]["message"]["content"]
