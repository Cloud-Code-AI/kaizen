import json
from pathlib import Path


class ConfigData:
    def __init__(self, config_data=None):
        config_file = "config.json"
        if Path(config_file).is_file():
            with open(config_file, "r") as f:
                self.config_data = json.loads(f.read())
        elif Path("~/.kaizen_config.json").is_file():
            with open("~/.kaizen_config.json", "r") as f:
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

    def get_config_data(self):
        return self.config_data

    def get_language_model_config(self):
        return self.config_data["language_model"]

    def get_github_app_config(self):
        return self.config_data["github_app"]
