from typing import Optional, List, Dict
import logging
from dataclasses import dataclass
import json

from kaizen.helpers import output, parser
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.code_review_prompts import (
    PR_DESCRIPTION_PROMPT,
    MERGE_PR_DESCRIPTION_PROMPT,
    PR_FILE_DESCRIPTION_PROMPT,
    PR_DESC_EVALUATION_PROMPT,
)


@dataclass
class DescOutput:
    desc: str
    usage: Dict[str, int]
    model_name: str
    cost: Dict[str, float]


class PRDescriptionGenerator:
    def __init__(self, llm_provider: LLMProvider):
        self.logger = logging.getLogger(__name__)
        self.provider = llm_provider

    def generate_pull_request_desc(
        self,
        diff_text: str,
        pull_request_title: str,
        pull_request_desc: str,
        pull_request_files: List[Dict],
        user: Optional[str] = None,
        reeval_response: bool = False,
    ) -> DescOutput:
        prompt = PR_DESCRIPTION_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=diff_text,
        )
        # TODO: User providers default usage
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        if self.provider.is_inside_token_limit(PROMPT=prompt):
            desc = self._process_full_diff(prompt, user, reeval_response, total_usage)
        else:
            desc = self._process_files(
                pull_request_files,
                pull_request_title,
                pull_request_desc,
                user,
                reeval_response,
                total_usage,
            )

        body = output.create_pr_description(desc, pull_request_desc)
        prompt_cost, completion_cost = self.provider.get_usage_cost(
            total_usage=total_usage
        )

        return DescOutput(
            desc=body,
            usage=total_usage,
            model_name=self.provider.model,
            cost={"prompt_cost": prompt_cost, "completion_cost": completion_cost},
        )

    def _process_full_diff(
        self,
        prompt: str,
        user: Optional[str],
        reeval_response: bool,
        total_usage: Dict[str, int],
    ) -> str:
        self.logger.debug("Processing directly from diff")
        resp, usage = self.provider.chat_completion(prompt, user=user)
        total_usage = self.provider.update_usage(total_usage, usage)

        if reeval_response:
            resp = self._reevaluate_response(prompt, resp, user, total_usage)

        desc_json = parser.extract_json(resp)
        return desc_json["desc"]

    def _process_files(
        self,
        pull_request_files: List[Dict],
        pull_request_title: str,
        pull_request_desc: str,
        user: Optional[str],
        reeval_response: bool,
        total_usage: Dict[str, int],
    ) -> str:
        self.logger.debug("Processing based on files")
        descs = []

        for file in pull_request_files:
            patch_details = file.get("patch")
            filename = file.get("filename", "")

            if (
                filename.split(".")[-1] not in parser.EXCLUDED_FILETYPES
                and patch_details is not None
            ):
                prompt = PR_FILE_DESCRIPTION_PROMPT.format(
                    PULL_REQUEST_TITLE=pull_request_title,
                    PULL_REQUEST_DESC=pull_request_desc,
                    CODE_DIFF=patch_details,
                )

                if not self.provider.is_inside_token_limit(PROMPT=prompt):
                    continue

                resp, usage = self.provider.chat_completion(prompt, user=user)
                total_usage = self.provider.update_usage(total_usage, usage)

                if reeval_response:
                    resp = self._reevaluate_response(prompt, resp, user, total_usage)

                desc_json = parser.extract_json(resp)
                descs.append(desc_json["desc"])

        prompt = MERGE_PR_DESCRIPTION_PROMPT.format(DESCS=json.dumps(descs))
        resp, usage = self.provider.chat_completion(prompt, user=user)
        total_usage = self.provider.update_usage(total_usage, usage)

        desc_json = parser.extract_json(resp)
        return desc_json["desc"]

    def _reevaluate_response(
        self, prompt: str, resp: str, user: Optional[str], total_usage: Dict[str, int]
    ) -> str:
        messages = [
            {"role": "system", "content": self.provider.system_prompt},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": resp},
            {"role": "user", "content": PR_DESC_EVALUATION_PROMPT},
        ]
        resp, usage = self.provider.chat_completion(
            prompt, user=user, messages=messages
        )
        total_usage = self.provider.update_usage(total_usage, usage)
        return resp
