from proctai.helpers import output, parser
from typing import Optional
from proctai.llms.provider import LLMProvider
from proctai.llms.prompts import (
    CODE_REVIEW_PROMPT,
    CODE_REVIEW_SYSTEM_PROMPT,
    PR_DESCRIPTION_PROMPT,
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
        user: Optional[str] = None,
    ):
        prompt = CODE_REVIEW_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=diff_text,
        )

        resp = self.provider.chat_completion(prompt, user=user)

        body = output.create_pr_review_from_json(parser.extract_json(resp))

        # Share the review on pull request
        return body

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

        resp = self.provider.chat_completion(prompt, user=user)
        self.logger.debug(f"PROMPT Generate PR Desc RESP: {resp}")
        body = output.create_pr_description(
            parser.extract_json(resp), pull_request_desc
        )
        return body
