from typing import Optional, List, Dict
from kaizen.llms.provider import LLMProvider
from kaizen.helpers import parser
from kaizen.llms.prompts.work_summary_prompts import (
    WORK_SUMMARY_PROMPT,
    WORK_SUMMARY_SYSTEM_PROMPT,
    TWITTER_POST_PROMPT,
    LINKEDIN_POST_PROMPT,
)
import logging


class WorkSummaryGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=WORK_SUMMARY_SYSTEM_PROMPT)

    def generate_work_summaries(
        self,
        diff_file_data: List[Dict],
        user: Optional[str] = None,
    ):
        available_tokens = self.provider.available_tokens(WORK_SUMMARY_PROMPT)
        summaries = []
        # Try to merge the files untill LLM can process the response
        combined_diff_data = ""
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        for file_dict in diff_file_data:
            temp_prompt = combined_diff_data
            temp_prompt += f"""\n---->\nFile Name: {file_dict["file"]}\nPatch: {file_dict["patch"]}\n Status: {file_dict["status"]}"""

            # If available tokens is greated than the new prompt size, process it.
            if available_tokens - self.provider.get_token_count(temp_prompt) > 0:
                combined_diff_data = temp_prompt
                continue

            # Process the prompt
            prompt = WORK_SUMMARY_PROMPT.format(PATCH_DATA=combined_diff_data)
            response, usage = self.provider.chat_completion(prompt, user=user)
            total_usage = self.provider.update_usage(total_usage, usage)
            summaries.append(parser.extract_json(response))
            combined_diff_data = ""

        if combined_diff_data != "":
            # process the remaining file diff pending
            prompt = WORK_SUMMARY_PROMPT.format(PATCH_DATA=combined_diff_data)
            response, usage = self.provider.chat_completion(prompt, user=user)
            summaries.append(parser.extract_json(response))
            combined_diff_data = ""
            total_usage = self.provider.update_usage(total_usage, usage)

        if len(summaries) > 1:
            # TODO Merge summaries
            pass

        return {"summary": summaries[0], "usage": total_usage}

    def generate_twitter_post(
        self,
        summary: Dict,
        user: Optional[str] = None,
    ) -> str:
        prompt = TWITTER_POST_PROMPT.format(SUMMARY=summary)
        response, total_usage = self.provider.chat_completion(prompt, user=user)
        return parser.extract_markdown_content(response), total_usage

    def generate_linkedin_post(
        self,
        summary: Dict,
        user: Optional[str] = None,
    ) -> str:
        prompt = LINKEDIN_POST_PROMPT.format(SUMMARY=summary)
        response, total_usage = self.provider.chat_completion(prompt, user=user)
        return parser.extract_markdown_content(response), total_usage
