from typing import Optional, List, Dict
import logging
from dataclasses import dataclass

from kaizen.helpers import output, parser
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.issue_analysis_prompts import (
    ISSUE_LABEL_PROMPT,
    ISSUE_DESC_PROMPT,
    ISSUE_LABEL_SYSTEM_PROMPT,
)


@dataclass
class IssueLabelOutput:
    labels: List[str]
    usage: Dict[str, int]
    model_name: str
    cost: Dict[str, float]


@dataclass
class IssueDescOutput:
    desc: str
    usage: Dict[str, int]
    model_name: str
    cost: Dict[str, float]


class IssueAnalysisGenerator:
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
    ) -> IssueLabelOutput:
        prompt = ISSUE_LABEL_PROMPT.format(
            ISSUE_LABEL_LIST=issue_label_list,
            ISSUE_TITLE=issue_title,
            ISSUE_DESCRIPTION=issue_desc,
        )
        if not issue_label_list and not issue_desc:
            raise Exception(
                "Issue labels missing for this repository. Create labels to ensure issue categorization."
            )

        if (
            issue_label_list
            and issue_desc
            and self.provider.is_inside_token_limit(PROMPT=prompt)
        ):
            labels = self._process_issue_for_labels(
                issue_title,
                issue_desc,
                user,
            )

        prompt_cost, completion_cost = self.provider.get_usage_cost(
            total_usage=self.total_usage
        )

        return IssueLabelOutput(
            labels=labels,
            usage=self.total_usage,
            model_name=self.provider.model,
            cost={"prompt_cost": prompt_cost, "completion_cost": completion_cost},
        )

    def generate_issue_desc(
        self,
        issue_title,
        issue_desc,
        user: Optional[str] = None,
    ) -> IssueDescOutput:
        prompt = ISSUE_DESC_PROMPT.format(
            ISSUE_TITLE=issue_title, ISSUE_DESC=issue_desc
        )
        if not issue_desc:
            raise Exception("Original issue description is empty!")

        if issue_desc and self.provider.is_inside_token_limit(PROMPT=prompt):
            desc = self._process_issue_for_desc(
                issue_title,
                issue_desc,
                user,
            )

        body = output.create_issue_description(desc, issue_desc)
        prompt_cost, completion_cost = self.provider.get_usage_cost(
            total_usage=self.total_usage
        )

        return IssueDescOutput(
            desc=body,
            usage=self.total_usage,
            model_name=self.provider.model,
            cost={"prompt_cost": prompt_cost, "completion_cost": completion_cost},
        )

    # TODO: Convert `labels` to a format suitable for the github handler
    def _process_issue_for_labels(
        self,
        prompt: str,
        user: Optional[str],
    ) -> List[str]:
        self.logger.debug("Processing Issue for labels")
        resp, usage = self.provider.chat_completion(
            prompt=prompt,
            user=user,
        )
        labels = parser.extract_code_from_markdown(resp)
        self.total_usage = self.provider.update_usage(self.total_usage, usage)

        return labels

    def _process_issue_for_desc(self, prompt: str, user: Optional[str]) -> str:
        self.logger.debug("Processing issue for description")
        resp, usage = self.provider.chat_completion(
            prompt=prompt,
            user=user,
        )
        desc = parser.extract_code_from_markdown(resp)
        self.total_usage = self.provider.update_usage(self.total_usage, usage)

        return desc
