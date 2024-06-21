from typing import Optional, List, Dict
from kaizen.helpers import output, parser
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.code_review_prompts import (
    CODE_REVIEW_PROMPT,
    CODE_REVIEW_SYSTEM_PROMPT,
    PR_DESCRIPTION_PROMPT,
    FILE_CODE_REVIEW_PROMPT,
    MERGE_PR_DESCRIPTION_PROMPT,
    PR_FILE_DESCRIPTION_PROMPT,
)
import logging
import json
from dataclasses import dataclass


@dataclass
class ReviewOutput:
    topics: dict
    usage: dict
    model_name: str
    cost: dict


@dataclass
class DescOutput:
    desc: str
    usage: dict
    model_name: str
    cost: dict


class CodeReviewer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=CODE_REVIEW_SYSTEM_PROMPT)

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
    ) -> ReviewOutput:

        # If diff_text is smaller than 70% of model token
        prompt = CODE_REVIEW_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=diff_text,
        )
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        if self.provider.is_inside_token_limit(PROMPT=prompt):
            self.logger.debug("Processing Directly from Diff")
            resp, usage = self.provider.chat_completion(prompt, user=user)
            review_json, total_usage = parser.extract_json_with_llm_retry(
                self.provider, resp, total_usage
            )
            reviews = review_json["review"]
            total_usage = self.provider.update_usage(total_usage, usage)
        else:
            self.logger.debug("Processing Based on files")
            # We recurrsively get feedback for files and then get basic summary
            reviews = []
            for file in pull_request_files:
                patch_details = file.get("patch")
                filename = file.get("filename", "")
                if (
                    filename.split(".")[-1] not in parser.EXCLUDED_FILETYPES
                    and patch_details is not None
                ):
                    prompt = FILE_CODE_REVIEW_PROMPT.format(
                        PULL_REQUEST_TITLE=pull_request_title,
                        PULL_REQUEST_DESC=pull_request_desc,
                        FILE_PATCH=patch_details,
                    )
                    if not self.provider.is_inside_token_limit(
                        PROMPT=prompt, percentage=85
                    ):
                        # TODO: Chunk this big files and process them
                        continue
                    resp, usage = self.provider.chat_completion(prompt, user=user)
                    total_usage = self.provider.update_usage(total_usage, usage)
                    review_json, total_usage = parser.extract_json_with_llm_retry(
                        self.provider, resp, total_usage
                    )
                    reviews.extend(review_json["review"])

        topics = self.merge_topics(reviews=reviews)
        # Share the review on pull request
        prompt_cost, completion_cost = self.provider.get_usage_cost(
            total_usage=total_usage
        )

        return ReviewOutput(
            usage=total_usage,
            model_name=self.provider.model,
            topics=topics,
            cost={"prompt_cost": prompt_cost, "completion_cost": completion_cost},
        )

    def generate_pull_request_desc(
        self,
        diff_text: str,
        pull_request_title: str,
        pull_request_desc: str,
        pull_request_files: List[Dict],
        user: Optional[str] = None,
    ):
        """
        This method generates a AI powered description for a pull request.
        """
        prompt = PR_DESCRIPTION_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=diff_text,
        )

        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        if self.provider.is_inside_token_limit(PROMPT=prompt):
            self.logger.debug("Processing Directly from Diff")
            resp, usage = self.provider.chat_completion(prompt, user=user)
            total_usage = self.provider.update_usage(total_usage, usage)
            json_data, total_usage = parser.extract_json_with_llm_retry(
                self.provider, resp, total_usage
            )
            desc = json_data["desc"]
        else:
            self.logger.debug("Processing Based on files")
            # We recurrsively get feedback for files and then get basic summary
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
                        # TODO: Chunk this big files and process them
                        continue
                    resp, usage = self.provider.chat_completion(prompt, user=user)
                    total_usage = self.provider.update_usage(total_usage, usage)
                    desc_json, total_usage = parser.extract_json_with_llm_retry(
                        self.provider, resp, total_usage
                    )
                    descs.append(desc_json["desc"])

            prompt = MERGE_PR_DESCRIPTION_PROMPT.format(DESCS=json.dumps(descs))
            resp, usage = self.provider.chat_completion(prompt, user=user)
            total_usage = self.provider.update_usage(total_usage, usage)
            resp, total_usage = parser.extract_json_with_llm_retry(
                self.provider, resp, total_usage
            )
            desc = resp["desc"]
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

    def merge_topics(self, reviews):
        topics = {}
        for review in reviews:
            if review["topic"] in topics:
                topics[review["topic"]].append(review)
            else:
                topics[review["topic"]] = [review]
        return topics

    def create_pr_review_text(self, topics):
        markdown_title = "## Code Review\n\n"
        markdown_output = ""
        high_ranked_issues = 0
        for topic, reviews in topics.items():
            if len(reviews) > 0:
                markdown_output += f"### {topic}\n\n"
                for review in reviews:
                    if review.get("confidence", "") == "critical":
                        high_ranked_issues += 1
                    ct = output.PR_COLLAPSIBLE_TEMPLATE.format(
                        comment=review.get("comment", "NA"),
                        reasoning=review.get("reasoning", "NA"),
                        solution=review.get("solution", "NA"),
                        confidence=review.get("confidence", "NA"),
                        start_line=review.get("start_line", "NA"),
                        end_line=review.get("end_line", "NA"),
                        file_name=review.get("file_name", "NA"),
                        request_for_change=review.get("request_for_change", "NA"),
                    )
                    markdown_output += ct + "\n"

        if high_ranked_issues > 0:
            status_msg = (
                "❗ **Attention Required:** This PR has potential issues. 🚨\n\n"
            )
        else:
            status_msg = "✅ **All Clear:** This PR is ready to merge! 👍\n\n"
        return markdown_title + status_msg + markdown_output
