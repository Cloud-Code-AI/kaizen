from typing import List, Dict, Optional
import logging
import json
from dataclasses import dataclass
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.code_fix_prompts import (
    CODE_FIX_SYSTEM_PROMPT,
    CODE_FIX_PROMPT,
)


@dataclass
class CodeFixerOutput:
    fixed_code: dict
    total_usage: dict


class CodeFixer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider()
        self.provider.system_prompt = (
            CODE_FIX_SYSTEM_PROMPT  # You'll need to define this
        )
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    def fix_code(
        self, original_code: str, issues: List[Dict], user: Optional[str] = None
    ) -> CodeFixerOutput:
        self.logger.info("Starting code fixing process")

        fix_prompt = CODE_FIX_PROMPT.format(
            file_content=original_code, issue_json=json.dumps(issues, indent=2)
        )

        if not self.provider.is_inside_token_limit(PROMPT=fix_prompt):
            self.logger.warning(f"Fix prompt for issue exceeds token limit. Skipping.")
            raise Exception("File Size too big!")

        resp, usage = self.provider.chat_completion_with_json(
            fix_prompt, user=user, model="best"
        )
        self.total_usage = self.provider.update_usage(self.total_usage, usage)

        return CodeFixerOutput(fixed_code=resp, total_usage=self.total_usage)
