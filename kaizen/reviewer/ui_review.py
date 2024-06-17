from typing import Optional, Dict
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.ui_reviewer_prompts import (
    UI_REVIEWER_PROMPT,
    UI_REVIEWER_SYSTEM_PROMPT,
)
import logging
from kaizen.helpers import output, parser


class UIReviewer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.provider = LLMProvider(system_prompt=UI_REVIEWER_SYSTEM_PROMPT)

    def generate_ui_review(
        self,
        url: str,
        user: Optional[str] = None,
    ) -> Dict:
        # Get HTML Data
        html = output.get_web_html(url)
        prompt = UI_REVIEWER_PROMPT.format(HTML_CODE=html)
        response, usage = self.provider.chat_completion(prompt, user=user)
        feedback = parser.extract_json(response).get("review", [])

        return {"reviews": feedback, "usage": usage}
