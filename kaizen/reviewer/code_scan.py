from typing import Optional, List, Dict
from dataclasses import dataclass
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.code_scan_prompts import (
    CODE_SCAN_SYSTEM_PROMPT,
    CODE_SCAN_PROMPT,
    CODE_SCAN_REEVALUATION_PROMPT,
)
from kaizen.helpers.patterns import ignore_patterns
import re
from pathlib import Path
import json
import logging
import fnmatch

compiled_patterns = [re.compile(pattern) for pattern in ignore_patterns]


@dataclass
class CodeScanOutput:
    issues: List[Dict]
    usage: Dict[str, int]
    model_name: str
    total_files: int
    files_processed: int


class CodeScanner:
    def __init__(self, llm_provider: LLMProvider):
        self.logger = logging.getLogger(__name__)
        self.provider = llm_provider
        # self.provider.model = self.provider.model_group_to_name["best"][0]
        self.provider.system_prompt = CODE_SCAN_SYSTEM_PROMPT
        self.reevaluate = False
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        self.logger.info(f"CodeScanner initialized with model: {self.provider.model}")

    def is_code_review_prompt_within_limit(self, file_data: str) -> bool:
        prompt = CODE_SCAN_PROMPT.format(FILE_DATA=file_data)
        result = self.provider.is_inside_token_limit(PROMPT=prompt)
        self.logger.debug(f"Prompt within token limit: {result}")
        return result

    def should_ignore(self, file_path):
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        should_ignore = any(
            fnmatch.fnmatch(file_path, pattern) for pattern in ignore_patterns
        )
        if should_ignore:
            self.logger.debug(f"Ignoring file: {file_path}")
        return should_ignore

    def review_code_dir(
        self,
        dir_path: str,
        reevaluate: bool = False,
        user: Optional[str] = None,
        max_files: Optional[int] = None,
    ):
        self.logger.info(f"Starting code review for directory: {dir_path}")
        self.reevaluate = reevaluate

        issues = []
        files_processed = 0
        for file_path in Path(dir_path).rglob("*.*"):
            if self.should_ignore(file_path):
                continue
            try:
                with open(str(file_path), "r") as f:
                    file_data = f.read()
                if max_files and files_processed >= max_files:
                    self.logger.info(f"Max files processed: {max_files}")
                    break
                self.logger.debug(f"Reviewing file: {file_path}")
                code_scan_output = self.review_code(file_data=file_data, user=user)
                files_processed += 1
                for issue in code_scan_output.issues:
                    issue["file_path"] = str(file_path)
                    issues.append(issue)
            except Exception as e:
                self.logger.error(
                    f"Error reviewing file {file_path}: {e}", exc_info=True
                )

        self.logger.info(f"Completed code review for directory: {dir_path}")
        return CodeScanOutput(
            usage=self.total_usage,
            model_name=self.provider.model,
            issues=issues,
            total_files=files_processed,
            files_processed=files_processed,
        )

    def review_code(self, file_data: str, user: Optional[str] = None) -> CodeScanOutput:
        self.logger.debug("Starting code review for file")
        prompt = CODE_SCAN_PROMPT.format(FILE_DATA=self._add_line_numbers(file_data))
        if not file_data:
            self.logger.error("file_data is empty!")
            raise Exception("file_data is empty!")

        if not self.provider.is_inside_token_limit(PROMPT=prompt):
            self.logger.error("file_data bigger than model token limit")
            raise Exception("file_data bigger than model token limit")

        issues = self._process_file_data(prompt, user)
        if self.reevaluate:
            self.logger.info("Starting reevaluation of issues")
            issues = self._reevaluate_issues(file_data, issues, user)
        self.logger.debug(f"Completed code review. Found {len(issues)} issues.")

        return CodeScanOutput(
            usage=self.total_usage,
            model_name=self.provider.model,
            issues=issues,
            total_files=1,
            files_processed=1,
        )

    def _process_file_data(self, prompt: str, user: Optional[str]) -> List[Dict]:
        self.logger.debug("Processing file data with LLM")
        resp, usage = self.provider.chat_completion_with_json(
            prompt, user=user, model="default"
        )
        self.total_usage = self.provider.update_usage(self.total_usage, usage)
        self.logger.info(f"LLM usage for this file: {usage}")
        return resp["issues"]

    def _reevaluate_issues(
        self, file_data: str, issues: List[Dict], user: Optional[str]
    ) -> List[Dict]:
        self.logger.debug("Reevaluating issues")
        reevaluation_prompt = CODE_SCAN_REEVALUATION_PROMPT.format(
            FILE_DATA=file_data, ISSUES=json.dumps({"issues": issues}, indent=2)
        )

        if not self.provider.is_inside_token_limit(PROMPT=reevaluation_prompt):
            self.logger.warning(
                "Reevaluation prompt exceeds token limit. Skipping reevaluation."
            )
            return issues

        resp, usage = self.provider.chat_completion_with_json(
            reevaluation_prompt, user=user, model="default"
        )
        self.total_usage = self.provider.update_usage(self.total_usage, usage)
        self.logger.info(f"LLM usage for reevaluation: {usage}")

        return resp.get("issues", issues)

    def _add_line_numbers(self, file_content):
        lines = file_content.split("\n")
        numbered_lines = [f"{i + 1:4d} | {line}" for i, line in enumerate(lines)]
        return "\n".join(numbered_lines)
