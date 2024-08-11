from typing import Optional, List, Dict
from kaizen.llms.provider import LLMProvider
from kaizen.helpers import parser
from kaizen.llms.prompts.work_summary_prompts import (
    WORK_SUMMARY_PROMPT,
    WORK_SUMMARY_SYSTEM_PROMPT,
    TWITTER_POST_PROMPT,
    LINKEDIN_POST_PROMPT,
    MERGE_WORK_SUMMARY_PROMPT,
)
import logging
import json


class WorkSummaryGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(
            system_prompt=WORK_SUMMARY_SYSTEM_PROMPT, default_temperature=0.1
        )
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    def generate_work_summaries(
        self,
        diff_file_data: List[Dict],
        user: Optional[str] = None,
    ):
        available_tokens = self.provider.available_tokens(WORK_SUMMARY_PROMPT)
        summaries = []
        # Try to merge the files untill LLM can process the response
        combined_diff_data = ""
        for file_dict in diff_file_data:
            temp_prompt = combined_diff_data
            temp_prompt += f"""\n---->\nFile Name: {file_dict["file"]}\nPatch: {file_dict["patch"]}\n Status: {file_dict["status"]}"""

            # If available tokens is greated than the new prompt size, process it.
            if available_tokens - self.provider.get_token_count(temp_prompt) > 0:
                combined_diff_data = temp_prompt
                continue

            # Process the prompt
            prompt = WORK_SUMMARY_PROMPT.format(PATCH_DATA=combined_diff_data)
            response, usage = self.provider.chat_completion_with_json(prompt, user=user)
            self.total_usage = self.provider.update_usage(self.total_usage, usage)
            summaries.append(response)
            combined_diff_data = ""

        if combined_diff_data != "":
            # process the remaining file diff pending
            prompt = WORK_SUMMARY_PROMPT.format(PATCH_DATA=combined_diff_data)
            response, usage = self.provider.chat_completion_with_json(prompt, user=user)
            summaries.append(response)
            combined_diff_data = ""
            self.total_usage = self.provider.update_usage(self.total_usage, usage)

        if len(summaries) > 1:
            # TODO Merge summaries
            prompt = MERGE_WORK_SUMMARY_PROMPT.format(
                SUMMARY_JSON=json.dumps(summaries)
            )
            response, usage = self.provider.chat_completion_with_json(prompt, user=user)
            summaries = [response]

        return {"summary": summaries[0], "usage": self.total_usage}

    def generate_twitter_post(
        self,
        summary: Dict,
        user: Optional[str] = None,
    ) -> str:
        prompt = TWITTER_POST_PROMPT.format(SUMMARY=summary)
        response, usage = self.provider.chat_completion(prompt, user=user)
        return parser.extract_markdown_content(response), usage

    def generate_linkedin_post(
        self,
        summary: Dict,
        user: Optional[str] = None,
    ) -> str:
        prompt = LINKEDIN_POST_PROMPT.format(SUMMARY=summary)
        response, usage = self.provider.chat_completion(prompt, user=user)
        return parser.extract_markdown_content(response), usage
