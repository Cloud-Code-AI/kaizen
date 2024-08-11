from typing import Optional, List, Dict, Generator
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

    def is_code_review_prompt_within_limit(
        self,
        diff_text: str,
        pull_request_title: str,
        pull_request_desc: str,
    ) -> bool:
        prompt = CODE_REVIEW_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=parser.patch_to_combined_chunks(diff_text),
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
        custom_prompt="",
    ) -> ReviewOutput:
        prompt = CODE_REVIEW_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            CODE_DIFF=parser.patch_to_combined_chunks(diff_text),
            CUSTOM_PROMPT=custom_prompt,
        )
        self.total_usage = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
        if not diff_text and not pull_request_files:
            raise Exception("Both diff_text and pull_request_files are empty!")

        if diff_text and self.provider.is_inside_token_limit(PROMPT=prompt):
            reviews = self._process_full_diff(prompt, user, reeval_response)
        else:
            reviews = self._process_files(
                pull_request_files,
                pull_request_title,
                pull_request_desc,
                user,
                reeval_response,
                custom_prompt=custom_prompt,
            )

        reviews.extend(self.check_sensitive_files(pull_request_files))

        topics = self._merge_topics(reviews)
        prompt_cost, completion_cost = self.provider.get_usage_cost(
            total_usage=self.total_usage
        )

        return ReviewOutput(
            usage=self.total_usage,
            model_name=self.provider.model,
            topics=topics,
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
        return resp["review"]

    def _process_files(
        self,
        pull_request_files: List[Dict],
        pull_request_title: str,
        pull_request_desc: str,
        user: Optional[str],
        reeval_response: bool,
        custom_prompt: str,
    ) -> List[Dict]:
        self.logger.debug("Processing based on files")
        reviews = []
        for file_review in self._process_files_generator(
            pull_request_files,
            pull_request_title,
            pull_request_desc,
            user,
            reeval_response,
            custom_prompt,
        ):
            reviews.extend(file_review)
        return reviews

    def _process_files_generator(
        self,
        pull_request_files: List[Dict],
        pull_request_title: str,
        pull_request_desc: str,
        user: Optional[str],
        reeval_response: bool,
        custom_prompt: str,
    ) -> Generator[List[Dict], None, None]:
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
                    + f"\n---->\nFile Name: {filename}\nPatch Details: {parser.patch_to_combined_chunks(patch_details)}"
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
                    custom_prompt,
                )
                combined_diff_data = (
                    f"\n---->\nFile Name: {filename}\nPatch Details: {patch_details}"
                )

        yield self._process_file_chunk(
            combined_diff_data,
            pull_request_title,
            pull_request_desc,
            user,
            reeval_response,
            custom_prompt,
        )

    def _process_file_chunk(
        self,
        diff_data: str,
        pull_request_title: str,
        pull_request_desc: str,
        user: Optional[str],
        reeval_response: bool,
        custom_prompt: str,
    ) -> List[Dict]:
        if not diff_data:
            return []
        prompt = FILE_CODE_REVIEW_PROMPT.format(
            PULL_REQUEST_TITLE=pull_request_title,
            PULL_REQUEST_DESC=pull_request_desc,
            FILE_PATCH=diff_data,
            CUSTOM_PROMPT=custom_prompt,
        )
        custom_model = {"model": self.default_model}
        resp, usage = self.provider.chat_completion_with_json(
            prompt, user=user, custom_model=custom_model
        )
        self.total_usage = self.provider.update_usage(self.total_usage, usage)

        if reeval_response:
            resp = self._reevaluate_response(prompt, resp, user)

        return resp["review"]

    def _reevaluate_response(self, prompt: str, resp: str, user: Optional[str]) -> str:
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
    def _merge_topics(reviews: List[Dict]) -> Dict[str, List[Dict]]:
        topics = {}
        for review in reviews:
            topics.setdefault(review["topic"], []).append(review)
        return topics

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
                                "topic": category,
                                "comment": "Changes made to sensitive file",
                                "confidence": "critical",
                                "reason": f"Changes were made to {file_name}, which needs review",
                                "solution": "NA",
                                "fixed_code": "",
                                "start_line": line,
                                "end_line": line,
                                "side": "RIGHT",
                                "file_name": file_name,
                                "sentiment": "negative",
                                "severity_level": 10,
                            }
                        )
        return reviews
