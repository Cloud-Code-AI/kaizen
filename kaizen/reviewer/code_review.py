from typing import Optional, List, Dict, Generator
from dataclasses import dataclass
import logging
from kaizen.helpers import parser
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.code_review_prompts import (
    CODE_REVIEW_PROMPT,
    FILE_CODE_REVIEW_PROMPT,
    PR_REVIEW_EVALUATION_PROMPT,
)


@dataclass
class ReviewOutput:
    topics: Dict[str, List[Dict]]
    usage: Dict[str, int]
    model_name: str
    cost: Dict[str, float]


class CodeReviewer:
    def __init__(self, llm_provider: LLMProvider):
        self.logger = logging.getLogger(__name__)
        self.provider = llm_provider

    def is_code_review_prompt_within_limit(
        self,
        diff_text: str,
        pull_request_title: str,
        pull_request_desc: str,
    ) -> bool:
        prompt = CODE_REVIEW_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=diff_text,
        )
        return self.provider.is_inside_token_limit(PROMPT=prompt)

    def review_pull_request(
        self,
        diff_text: str,
        pull_request_title: str,
        pull_request_desc: str,
        pull_request_files: List[Dict],
        user: Optional[str] = None,
        reeval_response: bool = False,
    ) -> ReviewOutput:
        prompt = CODE_REVIEW_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=diff_text,
        )
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        if self.provider.is_inside_token_limit(PROMPT=prompt):
            reviews = self._process_full_diff(
                prompt, user, reeval_response, total_usage
            )
        else:
            reviews = self._process_files(
                pull_request_files,
                pull_request_title,
                pull_request_desc,
                user,
                reeval_response,
                total_usage,
            )

        topics = self._merge_topics(reviews)
        prompt_cost, completion_cost = self.provider.get_usage_cost(
            total_usage=total_usage
        )

        return ReviewOutput(
            usage=total_usage,
            model_name=self.provider.model,
            topics=topics,
            cost={"prompt_cost": prompt_cost, "completion_cost": completion_cost},
        )

    def _process_full_diff(
        self,
        prompt: str,
        user: Optional[str],
        reeval_response: bool,
        total_usage: Dict[str, int],
    ) -> List[Dict]:
        self.logger.debug("Processing directly from diff")
        resp, usage = self.provider.chat_completion(prompt, user=user)
        total_usage = self.provider.update_usage(total_usage, usage)

        if reeval_response:
            resp = self._reevaluate_response(prompt, resp, user, total_usage)

        review_json = parser.extract_json(resp)
        return review_json["review"]

    def _process_files(
        self,
        pull_request_files: List[Dict],
        pull_request_title: str,
        pull_request_desc: str,
        user: Optional[str],
        reeval_response: bool,
        total_usage: Dict[str, int],
    ) -> List[Dict]:
        self.logger.debug("Processing based on files")
        reviews = []
        for file_review in self._process_files_generator(
            pull_request_files,
            pull_request_title,
            pull_request_desc,
            user,
            reeval_response,
            total_usage,
        ):
            reviews.extend(file_review)
        return reviews

    def _process_files_generator(
        self,
        pull_request_files: List[Dict],
        pull_request_title: str,
        pull_request_desc: str,
        user: Optional[str],
        reeval_response: bool,
        total_usage: Dict[str, int],
    ) -> Generator[List[Dict], None, None]:
        combined_diff_data = ""
        available_tokens = self.provider.available_tokens(FILE_CODE_REVIEW_PROMPT)

        for file in pull_request_files:
            patch_details = file.get("patch")
            filename = file.get("filename", "")

            if (
                filename.split(".")[-1] not in parser.EXCLUDED_FILETYPES
                and patch_details is not None
            ):
                temp_prompt = (
                    combined_diff_data
                    + f"\n---->\nFile Name: {filename}\nPatch Details: {patch_details}"
                )

                if available_tokens - self.provider.get_token_count(temp_prompt) > 0:
                    combined_diff_data = temp_prompt
                    continue

                yield self._process_file_chunk(
                    combined_diff_data,
                    pull_request_title,
                    pull_request_desc,
                    user,
                    reeval_response,
                    total_usage,
                )
                combined_diff_data = (
                    f"\n---->\nFile Name: {filename}\nPatch Details: {patch_details}"
                )

        if combined_diff_data:
            yield self._process_file_chunk(
                combined_diff_data,
                pull_request_title,
                pull_request_desc,
                user,
                reeval_response,
                total_usage,
            )

    def _process_file_chunk(
        self,
        diff_data: str,
        pull_request_title: str,
        pull_request_desc: str,
        user: Optional[str],
        reeval_response: bool,
        total_usage: Dict[str, int],
    ) -> List[Dict]:
        prompt = FILE_CODE_REVIEW_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            FILE_PATCH=diff_data,
        )
        resp, usage = self.provider.chat_completion(prompt, user=user)
        total_usage = self.provider.update_usage(total_usage, usage)

        if reeval_response:
            resp = self._reevaluate_response(prompt, resp, user, total_usage)

        review_json = parser.extract_json(resp)
        return review_json["review"]

    def _reevaluate_response(
        self, prompt: str, resp: str, user: Optional[str], total_usage: Dict[str, int]
    ) -> str:
        messages = [
            {"role": "system", "content": self.provider.system_prompt},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": resp},
            {"role": "user", "content": PR_REVIEW_EVALUATION_PROMPT},
        ]
        resp, usage = self.provider.chat_completion(
            prompt, user=user, messages=messages
        )
        total_usage = self.provider.update_usage(total_usage, usage)
        return resp

    @staticmethod
    def _merge_topics(reviews: List[Dict]) -> Dict[str, List[Dict]]:
        topics = {}
        for review in reviews:
            topics.setdefault(review["topic"], []).append(review)
        return topics
