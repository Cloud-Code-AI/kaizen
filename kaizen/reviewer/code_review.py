from kaizen.helpers import output, parser
from typing import Optional, List, Dict
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts import (
    CODE_REVIEW_PROMPT,
    CODE_REVIEW_SYSTEM_PROMPT,
    PR_DESCRIPTION_PROMPT,
    FILE_CODE_REVIEW_PROMPT,
)
import logging


class CodeReviewer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=CODE_REVIEW_SYSTEM_PROMPT)

    def review_pull_request(
        self,
        diff_text: str,
        pull_request_title: str,
        pull_request_desc: str,
        pull_request_files: List[Dict],
        user: Optional[str] = None,
    ):

        # If diff_text is smaller than 70% of model token
        prompt = CODE_REVIEW_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=diff_text,
        )
        total_usage = None
        if self.provider.is_inside_token_limit(PROMPT=prompt):
            self.logger.debug("Processing Directly from Diff")
            resp, usage = self.provider.chat_completion(prompt, user=user)
            review_json = parser.extract_json(resp)
            reviews = review_json["review"]
            total_usage = self.provider.update_usage(total_usage, usage)
        else:
            self.logger.debug("Processing Based on files")
            # We recurrsively get feedback for files and then get basic summary
            reviews = []
            for file in pull_request_files:
                patch_details = file["patch"]
                filename = file["filename"]
                if filename.split(".")[-1] not in parser.EXCLUDED_FILETYPES:
                    prompt = FILE_CODE_REVIEW_PROMPT.format(
                        PULL_REQUEST_TITLE=pull_request_title,
                        PULL_REQUEST_DESC=pull_request_desc,
                        FILE_PATCH=patch_details,
                    )
                    resp, usage = self.provider.chat_completion(prompt, user=user)
                    total_usage = self.provider.update_usage(total_usage, usage)
                    review_json = parser.extract_json(resp)
                    reviews.extend(review_json["review"])
        body = output.create_pr_review_from_json(reviews)
        self.logger.debug(f"Generated Review:\n {body}")
        # Share the review on pull request

        return {"review": body, "usage": total_usage}

    def generate_pull_request_desc(
        self,
        diff_text: str,
        pull_request_title: str,
        pull_request_desc: str,
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

        # TODO: split the diff if alot of files and contents.
        resp, usage = self.provider.chat_completion(prompt, user=user)
        total_usage = None
        self.logger.debug(f"PROMPT Generate PR Desc RESP: {resp}")
        body = output.create_pr_description(
            parser.extract_json(resp), pull_request_desc
        )
        total_usage = self.provider.update_usage(total_usage, usage)
        return {"desc": body, "usage": total_usage}
