from typing import Optional, List, Dict, Generator, Tuple
from dataclasses import dataclass
import logging
from kaizen.helpers import parser
from kaizen.llms.provider import LLMProvider
from kaizen.llms.prompts.code_review_prompts import (
    CODE_REVIEW_PROMPT,
    FILE_CODE_REVIEW_PROMPT,
    PR_REVIEW_EVALUATION_PROMPT,
    CODE_REVIEW_SYSTEM_PROMPT,
)
import json
import fnmatch

sensitive_files = {
    "Configuration": [
        ".env",
        ".config",
        "config.json",
        "config.yaml",
        "config.yml",
        ".ini",
        ".toml",
        "settings.py",
    ],
    "Build and Dependency": [
        "requirements.txt",
        "Pipfile",
        "Pipfile.lock",
        "package.json",
        "package-lock.json",
        "yarn.lock",
        "Gemfile",
        "Gemfile.lock",
        "pom.xml",
        "build.gradle",
    ],
    "CI/CD": [
        ".travis.yml",
        ".gitlab-ci.yml",
        "Jenkinsfile",
        ".circleci/config.yml",
        ".github/workflows/*.yml",
    ],
    "Docker": [
        "Dockerfile",
        "docker-compose.yml",
        ".dockerignore",
    ],
    "Version Control": [
        ".gitignore",
        ".gitattributes",
        ".gitmodules",
    ],
    "Security": [
        "security.txt",
        ".htaccess",
        "robots.txt",
    ],
    "Database": [
        "*.sql",
        "schema.rb",
        "migrations/*.rb",
        "alembic/versions/*.py",
    ],
    "Documentation": [
        "README.md",
        "CHANGELOG.md",
        "LICENSE",
        "CONTRIBUTING.md",
    ],
    "Infrastructure as Code": [
        "*.tf",  # Terraform
        "*.hcl",  # Hashicorp Configuration Language
        "cloudformation.yaml",
        "*.template",  # AWS CloudFormation
    ],
    "Sensitive Data": [
        "*.pem",
        "*.key",
        "*.cer",
        "*.crt",
    ],
}


@dataclass
class ReviewOutput:
    topics: Dict[str, List[Dict]]
    issues: List[Dict]
    code_quality: float
    usage: Dict[str, int]
    model_name: str
    cost: Dict[str, float]


class CodeReviewer:
    def __init__(self, llm_provider: LLMProvider, default_model="default"):
        self.logger = logging.getLogger(__name__)
        self.provider = llm_provider
        self.provider.system_prompt = CODE_REVIEW_SYSTEM_PROMPT
        self.default_model = default_model
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        self.ignore_deletions = False

    def is_code_review_prompt_within_limit(
        self,
        diff_text: str,
        pull_request_title: str,
        pull_request_desc: str,
    ) -> bool:
        prompt = CODE_REVIEW_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=parser.patch_to_combined_chunks(
                diff_text, ignore_deletions=self.ignore_deletions
            ),
        )
        return self.provider.is_inside_token_limit(PROMPT=prompt)

    def review_pull_request(
        self,
        diff_text: str,
        pull_request_title: str,
        pull_request_desc: str,
        pull_request_files: List[Dict],
        user: Optional[str] = None,
        reeval_response: bool = False,
        model="default",
        ignore_deletions=False,
        custom_context: str = "",
        check_sensetive: bool = False,
    ) -> ReviewOutput:
        self.ignore_deletions = ignore_deletions
        prompt = (
            CODE_REVIEW_PROMPT.format(
                CODE_DIFF=parser.patch_to_combined_chunks(
                    diff_text, self.ignore_deletions
                ),
            )
            + custom_context
        )
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        if not diff_text and not pull_request_files:
            raise Exception("Both diff_text and pull_request_files are empty!")

        if diff_text and self.provider.is_inside_token_limit(PROMPT=prompt):
            reviews, code_quality = self._process_full_diff(
                prompt, user, reeval_response
            )
        else:
            reviews, code_quality = self._process_files(
                pull_request_files,
                pull_request_title,
                pull_request_desc,
                user,
                reeval_response,
                custom_context,
            )
        if check_sensetive:
            reviews.extend(self.check_sensitive_files(pull_request_files))

        categories = self._merge_categories(reviews)
        prompt_cost, completion_cost = self.provider.get_usage_cost(
            total_usage=self.total_usage
        )

        return ReviewOutput(
            usage=self.total_usage,
            model_name=self.provider.model,
            topics=categories,
            issues=reviews,
            code_quality=code_quality,
            cost={"prompt_cost": prompt_cost, "completion_cost": completion_cost},
        )

    def _process_full_diff(
        self,
        prompt: str,
        user: Optional[str],
        reeval_response: bool,
    ) -> List[Dict]:
        self.logger.debug("Processing directly from diff")
        custom_model = {"model": self.default_model}
        resp, usage = self.provider.chat_completion_with_json(
            prompt, user=user, custom_model=custom_model
        )
        self.total_usage = self.provider.update_usage(self.total_usage, usage)
        if reeval_response:
            resp = self._reevaluate_response(prompt, resp, user)
        return resp["review"], resp.get("code_quality_percentage", None)

    def _process_files(
        self,
        pull_request_files: List[Dict],
        pull_request_title: str,
        pull_request_desc: str,
        user: Optional[str],
        reeval_response: bool,
        custom_context: str,
    ) -> Tuple[List[Dict], Optional[float]]:
        self.logger.debug("Processing based on files")
        reviews = []
        code_quality = None
        file_chunks_generator = self._process_files_generator(
            pull_request_files,
            pull_request_title,
            pull_request_desc,
            user,
            reeval_response,
            custom_context,
        )
        for result in file_chunks_generator:
            if result:  # Check if the result is not None
                file_review, quality = result
                reviews.extend(file_review)
                if quality:
                    if code_quality is None or quality < code_quality:
                        code_quality = quality
        return reviews, code_quality

    def _process_files_generator(
        self,
        pull_request_files: List[Dict],
        pull_request_title: str,
        pull_request_desc: str,
        user: Optional[str],
        reeval_response: bool,
        custom_context: str,
    ) -> Generator[Optional[Tuple[List[Dict], Optional[float]]], None, None]:
        combined_diff_data = ""
        available_tokens = self.provider.available_tokens(FILE_CODE_REVIEW_PROMPT)
        for file in pull_request_files:
            patch_details = file.get("patch")
            filename = file.get("filename", "").replace(" ", "")

            if (
                filename.split(".")[-1] not in parser.EXCLUDED_FILETYPES
                and patch_details is not None
            ):
                temp_prompt = (
                    combined_diff_data
                    + f"\n---->\nFile Name: {filename}\nPatch Details: {parser.patch_to_combined_chunks(patch_details, self.ignore_deletions)}"
                )

                if available_tokens - self.provider.get_token_count(temp_prompt) > 0:
                    combined_diff_data = temp_prompt
                    continue

                yield self._process_file_chunk(
                    combined_diff_data,
                    pull_request_title,
                    pull_request_desc,
                    user,
                    reeval_response,
                    custom_context,
                )
                combined_diff_data = f"\n---->\nFile Name: {filename}\nPatch Details: {parser.patch_to_combined_chunks(patch_details,  self.ignore_deletions)}"

        if combined_diff_data:
            yield self._process_file_chunk(
                combined_diff_data,
                pull_request_title,
                pull_request_desc,
                user,
                reeval_response,
                custom_context,
            )
        else:
            yield None  # Yield None if there's no data to process

    def _process_file_chunk(
        self,
        diff_data: str,
        pull_request_title: str,
        pull_request_desc: str,
        user: Optional[str],
        reeval_response: bool,
        custom_context: str,
    ) -> Optional[Tuple[List[Dict], Optional[float]]]:
        if not diff_data:
            return None
        prompt = (
            FILE_CODE_REVIEW_PROMPT.format(
                FILE_PATCH=diff_data,
            )
            + custom_context
        )
        custom_model = {"model": self.default_model}
        resp, usage = self.provider.chat_completion_with_json(
            prompt, user=user, custom_model=custom_model
        )
        self.total_usage = self.provider.update_usage(self.total_usage, usage)

        if reeval_response:
            resp = self._reevaluate_response(prompt, resp, custom_context, user)

        return resp.get("review", []), resp.get("code_quality_percentage", None)

    def _reevaluate_response(
        self, prompt: str, resp: str, custom_context: str, user: Optional[str]
    ) -> str:
        new_prompt = PR_REVIEW_EVALUATION_PROMPT.format(
            ACTUAL_PROMPT=prompt, LLM_OUTPUT=json.dumps(resp)
        )
        messages = [
            {"role": "system", "content": self.provider.system_prompt},
            {"role": "user", "content": new_prompt},
        ]
        custom_model = {"model": self.default_model}
        resp, usage = self.provider.chat_completion_with_json(
            new_prompt, user=user, messages=messages, custom_model=custom_model
        )
        self.total_usage = self.provider.update_usage(self.total_usage, usage)
        return resp

    @staticmethod
    def _merge_categories(reviews: List[Dict]) -> Dict[str, List[Dict]]:
        categories = {}
        for review in reviews:
            categories.setdefault(review["category"], []).append(review)
        return categories

    def check_sensitive_files(self, pull_request_files: list):
        reviews = []

        for category, patterns in sensitive_files.items():
            for patch_data in pull_request_files:
                file_name = patch_data.get("filename", "").replace(" ", "")
                for pattern in patterns:
                    if fnmatch.fnmatch(file_name, pattern):
                        patch = patch_data.get("patch", "")
                        line = 1
                        if patch:
                            line = patch.split(" ")[2].split(",")[0][1:]
                        reviews.append(
                            {
                                "category": category,
                                "description": "Changes made to sensitive file",
                                "impact": "critical",
                                "recommendation": f"Changes were made to {file_name}, which needs review",
                                "current_code": "NA",
                                "fixed_code": "",
                                "start_line": line,
                                "end_line": line,
                                "side": "RIGHT",
                                "file_path": file_name,
                                "sentiment": "negative",
                                "severity": 10,
                            }
                        )
        return reviews
