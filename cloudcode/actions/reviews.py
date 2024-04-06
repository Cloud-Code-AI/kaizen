from cloudcode.helpers import output, parser
from cloudcode.llms.provider import LLMProvider
from cloudcode.llms.prompts import CODE_REVIEW_PROMPT, CODE_REVIEW_SYSTEM_PROMPT
import logging


class CodeReviewer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=CODE_REVIEW_SYSTEM_PROMPT)

    def review_pull_request(
        self, diff_text: str, pull_request_title: str, pull_request_desc: str
    ):
        prompt = CODE_REVIEW_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=diff_text,
        )

        resp = self.provider.chat_completion(prompt)

        body = output.json_to_markdown(parser.extract_json(resp))

        # Share the review on pull request
        return body
