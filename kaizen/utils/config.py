import json
from pathlib import Path
import os


class ConfigData:
    def __init__(self, config_data=None):
        config_local_path = "config.json"
        config_file_path = os.path.expanduser("~/.kaizen_config.json")
        if Path(config_local_path).is_file():
            with open(config_local_path, "r") as f:
                self.config_data = json.loads(f.read())
        elif Path(config_file_path).is_file():
            with open(config_file_path, "r") as f:
                self.config_data = json.loads(f.read())
        else:
            self.config_data = {
                "language_model": {
                    "provider": "litellm",
                    "enable_observability_logging": False,
                    "models": [
                        {
                            "model_name": "default",
                            "litellm_params": {"model": "gpt-4o-mini"},
                        },
                    ],
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

    def get_config_data(self):
        return self.config_data

    def get_language_model_config(self):
        return self.config_data["language_model"]

    def get_github_app_config(self):
        return self.config_data["github_app"]
