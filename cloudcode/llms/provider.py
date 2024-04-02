from litellm import completion
from cloudcode.llms.prompts import BASIC_SYSTEM_PROMPT


def chat_completion(
    prompt: str,
    system_prompt: str = BASIC_SYSTEM_PROMPT,
    model: str = "gpt-3.5-turbo-1106",
    max_tokens: int = 1000,
    temperature: float = 0,
):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    response = completion(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response["choices"][0]["message"]["content"]
