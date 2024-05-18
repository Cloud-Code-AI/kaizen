import json
import os
from pathlib import Path


class ConfigData:
    def __init__(self, config_data=None):
        config_file = "config.json"
        if Path(config_file).is_file():
            with open(config_file, "r") as f:
                self.config_data = json.loads(f.read())
        else:
            print(f"Couldnt find config at {config_file} loading default vals")
            self.config_data = {
                "language_model": {
                    "provider": "litellm",
                    "enable_observability_logging": False,
                },
                "github_app": {
                    "check_signature": False,
                    "auto_pr_review": False,
                    "edit_pr_desc": False,
                },
            }

        if config_data:
            self.update_config_data(config_data)

    def update_config_data(self, new_config_data):
        self.config_data.update(new_config_data)
        self.validate_config_settings(self.config_data)

    def get_config_data(self):
        return self.config_data

    def get_language_model_config(self):
        return self.config_data["language_model"]

    def get_github_app_config(self):
        return self.config_data["github_app"]

    def validate_config_settings(self):
        "Make sure relvant enviorment variables are set"
        if self.config_data.get("github_app", {}).get("check_signature", False):
            if not os.environ.get("GITHUB_APP_WEBHOOK_SECRET"):
                raise EnvironmentError(
                    "The environment variable 'GITHUB_APP_WEBHOOK_SECRET' is not set."
                )

        if self.config_data.get("language_model", {}).get("provider", {}) == "litellm":
            if self.config_data.get("language_model", {}).get(
                "enable_observability_logging", False
            ):
                if not os.environ.get("SUPABASE_URL"):
                    raise EnvironmentError(
                        "The environment variable 'SUPABASE_URL' is not set."
                    )
                if not os.environ.get("SUPABASE_KEY"):
                    raise EnvironmentError(
                        "The environment variable 'SUPABASE_KEY' is not set."
                    )
