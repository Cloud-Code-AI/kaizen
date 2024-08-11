from typing import Optional, List, Dict, Generator
from dataclasses import dataclass
import logging
from kaizen.helpers import parser
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.ask_question_prompts import (
    ANSWER_QUESTION_SYSTEM_PROMPT,
    ANSWER_QUESTION_PROMPT,
    FILE_ANSWER_QUESTION_PROMPT,
    SUMMARIZE_ANSWER_PROMPT,
)


@dataclass
class AnswerOutput:
    answer: str
    usage: Dict[str, int]
    model_name: str
    cost: Dict[str, float]


class QuestionAnswer:
    def __init__(self, llm_provider: LLMProvider):
        self.logger = logging.getLogger(__name__)
        self.provider = llm_provider
        self.provider.system_prompt = ANSWER_QUESTION_SYSTEM_PROMPT
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }

    def is_ask_question_prompt_within_limit(
        self,
        diff_text: str,
        pull_request_title: str,
        pull_request_desc: str,
        question: str,
    ) -> bool:
        prompt = ANSWER_QUESTION_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=parser.patch_to_combined_chunks(diff_text),
            QUESTION=question,
        )
        return self.provider.is_inside_token_limit(PROMPT=prompt)

    def ask_pull_request(
        self,
        diff_text: str,
        pull_request_title: str,
        pull_request_desc: str,
        question: str,
        pull_request_files: List[Dict],
        user: Optional[str] = None,
    ) -> AnswerOutput:
        prompt = ANSWER_QUESTION_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=parser.patch_to_combined_chunks(diff_text),
            QUESTION=question,
        )
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        if not diff_text and not pull_request_files:
            raise Exception("Both diff_text and pull_request_files are empty!")

        if diff_text and self.provider.is_inside_token_limit(PROMPT=prompt):
            resp = self._process_full_diff_qa(prompt, user)

        else:
            resp = self._process_files_qa(
                pull_request_files,
                pull_request_title,
                pull_request_desc,
                question,
                user,
            )

        prompt_cost, completion_cost = self.provider.get_usage_cost(
            total_usage=self.total_usage
        )

        return AnswerOutput(
            answer=resp,
            usage=self.total_usage,
            model_name=self.provider.model,
            cost={"prompt_cost": prompt_cost, "completion_cost": completion_cost},
        )

    def _process_full_diff_qa(
        self,
        prompt: str,
        user: Optional[str],
    ) -> str:
        self.logger.debug("Processing directly from diff")
        resp, usage = self.provider.chat_completion(prompt, user=user)
        self.total_usage = self.provider.update_usage(self.total_usage, usage)
        return resp

    def _process_files_qa(
        self,
        pull_request_files: List[Dict],
        pull_request_title: str,
        pull_request_desc: str,
        question: str,
        user: Optional[str],
    ) -> str:
        self.logger.debug("Processing based on files")
        responses = []
        for answer in self._process_files_generator_qa(
            pull_request_files,
            pull_request_title,
            pull_request_desc,
            question,
            user,
        ):
            responses.append(answer)
            ## summarize responses
        return self._summarize_responses(question, responses)

    def _process_files_generator_qa(
        self,
        pull_request_files: List[Dict],
        pull_request_title: str,
        pull_request_desc: str,
        question: str,
        user: Optional[str],
    ) -> Generator[str, None, None]:
        combined_diff_data = ""
        available_tokens = self.provider.available_tokens(FILE_ANSWER_QUESTION_PROMPT)

        for file in pull_request_files:
            patch_details = file.get("patch")
            filename = file.get("filename", "")

            if (
                filename.split(".")[-1] not in parser.EXCLUDED_FILETYPES
                and patch_details is not None
            ):
                temp_prompt = (
                    combined_diff_data
                    + f"\n---->\nFile Name: {filename}\nPatch Details: {parser.patch_to_combined_chunks(patch_details)}"
                )

                if available_tokens - self.provider.get_token_count(temp_prompt) > 0:
                    combined_diff_data = temp_prompt
                    continue

                yield self._process_file_chunk_qa(
                    combined_diff_data,
                    pull_request_title,
                    pull_request_desc,
                    question,
                    user,
                )
                combined_diff_data = (
                    f"\n---->\nFile Name: {filename}\nPatch Details: {patch_details}"
                )

        if combined_diff_data:
            yield self._process_file_chunk_qa(
                combined_diff_data,
                pull_request_title,
                pull_request_desc,
                question,
                user,
            )

    def _process_file_chunk_qa(
        self,
        diff_data: str,
        pull_request_title: str,
        pull_request_desc: str,
        question: str,
        user: Optional[str],
    ) -> str:
        if not diff_data:
            return ""
        prompt = FILE_ANSWER_QUESTION_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            FILE_PATCH=diff_data,
            QUESTION=question,
        )
        resp, usage = self.provider.chat_completion(prompt, user=user)
        self.total_usage = self.provider.update_usage(self.total_usage, usage)
        return resp

    def _summarize_responses(self, question: str, responses: List[str]) -> str:
        if len(responses) == 1:
            return responses[0]

        formatted_responses = "\n\n".join(
            f"Response for file/chunk {i + 1}:\n{response}"
            for i, response in enumerate(responses)
        )
        summary_prompt = SUMMARIZE_ANSWER_PROMPT.format(
            QUESTION=question, RESPONSES=formatted_responses
        )

        summarized_answer, usage = self.provider.chat_completion(summary_prompt)
        self.total_usage = self.provider.update_usage(self.total_usage, usage)

        return summarized_answer
