from codecheck.helpers import output, parser
from codecheck.llms.provider import chat_completion
from codecheck.llms.prompts import CODE_REVIEW_PROMPT, CODE_REVIEW_SYSTEM_PROMPT
import logging

logger = logging.getLogger(__name__)


def review_pull_request(
    diff_text: str,
    pull_request_title: str,
    pull_request_desc: str,
):
    prompt = CODE_REVIEW_PROMPT.format(
        PULL_REQUEST_TITLE=pull_request_title,
        PULL_REQUEST_DESC=pull_request_desc,
        CODE_DIFF=diff_text,
    )

    logger.info("Code Review Prompt: ", prompt)

    resp = chat_completion(
        prompt,
        system_prompt=CODE_REVIEW_SYSTEM_PROMPT,
    )

    body = output.json_to_markdown(parser.extract_json(resp))

    # Share the review on pull request
    return body
