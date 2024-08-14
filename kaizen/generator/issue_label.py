from typing import Optional, List, Dict, Generator
import logging
from dataclasses import dataclass
import json

from kaizen.helpers import output, parser
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.issue_label_prompts import (
    ISSUE_LABEL_PROMPT,
    ISSUE_LABEL_SYSTEM_PROMPT,
)

@dataclass
class LabelOutput:
    labels: List[str]
    usage: Dict[str, int]
    model_name: str
    cost: Dict[str, float]
    
class IssueLabelGenerator:
    def __init__(self, llm_provider: LLMProvider):
        self.logger = logging.getLogger(__name__)
        self.provider = llm_provider
        self.provider.system_prompt = ISSUE_LABEL_SYSTEM_PROMPT
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
    
    def generate_issue_labels(
        self,
        issue_label_list: List[str],
        issue_title: str,
        issue_desc: str,
        user: Optional[str] = None,
    ) -> LabelOutput:
        prompt = ISSUE_LABEL_PROMPT.format(
            ISSUE_LABEL_LIST=issue_label_list,
            ISSUE_TITLE=issue_title,
            ISSUE_DESCRIPTION=issue_desc,
        )
        if not issue_label_list:
            raise Exception("Issue labels missing for this repository. Create labels to ensure issue categorization.")

        if issue_label_list and self.provider.is_inside_token_limit(PROMPT=prompt):
            labels = self._process_issue(
                issue_title,
                issue_desc,
                user,
            )
        
        prompt_cost, completion_cost = self.provider.get_usage_cost(
            total_usage=self.total_usage
        )
        
        return LabelOutput(
            labels=labels,
            usage=self.total_usage,
            model_name=self.provider.model,
            cost={"prompt_cost": prompt_cost, "completion_cost": completion_cost}
        )
    
    def _process_issue(
        self,
        prompt: str,
        user: Optional[str],
    ) -> List[str]:
        self.logger.debug("Processing Issue")
        resp, usage = self.provider.chat_completion(
            prompt=prompt,
            user=user,
        )
        labels = parser.extract_code_from_markdown(resp)
        # TODO: Convert `labels` to a format suitable for the github handler
        self.total_usage = self.provider.update_usage(self.total_usage, usage)
        
        return labels