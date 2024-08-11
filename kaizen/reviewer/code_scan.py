from typing import Optional, List, Dict
from dataclasses import dataclass
import logging
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.code_scan_prompts import (
    CODE_SCAN_SYSTEM_PROMPT,
    CODE_SCAN_PROMPT,
)


@dataclass
class CodeScanOutput:
    issues: Dict[str, List[Dict]]
    usage: Dict[str, int]
    model_name: str
    cost: Dict[str, float]


class CodeScanner:
    def __init__(self, llm_provider: LLMProvider):
        self.logger = logging.getLogger(__name__)
        self.provider = llm_provider
        self.provider.model = self.provider.model_group_to_name["best"][0]
        self.provider.system_prompt = CODE_SCAN_SYSTEM_PROMPT
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    def is_code_review_prompt_within_limit(
        self,
        file_data: str,
    ) -> bool:
        prompt = CODE_SCAN_PROMPT.format(FILE_DATA=file_data)
        return self.provider.is_inside_token_limit(PROMPT=prompt)

    def review_code(
        self,
        file_data: str,
        user: Optional[str] = None,
    ) -> CodeScanOutput:
        prompt = CODE_SCAN_PROMPT.format(
            FILE_DATA=file_data,
        )
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        if not file_data:
            raise Exception("file_data is empty!")

        if not self.provider.is_inside_token_limit(PROMPT=prompt):
            raise Exception("file_data bigger than model token limit")

        issues = self._process_file_data(prompt, user)

        prompt_cost, completion_cost = self.provider.get_usage_cost(
            total_usage=self.total_usage
        )

        return CodeScanOutput(
            usage=self.total_usage,
            model_name=self.provider.model,
            issues=issues,
            cost={"prompt_cost": prompt_cost, "completion_cost": completion_cost},
        )

    def _process_file_data(
        self,
        prompt: str,
        user: Optional[str],
    ) -> List[Dict]:
        resp, usage = self.provider.chat_completion_with_json(
            prompt, user=user, model="best"
        )
        self.total_usage = self.provider.update_usage(self.total_usage, usage)
        return resp["issues"]
