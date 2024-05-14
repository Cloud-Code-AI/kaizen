import json
import os
from pathlib import Path


def get_config():
    # Get the directory of the calling function
    caller_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    config_file = f"{caller_dir}/config.json"
    if Path(config_file).is_file():
        with open(config_file, "r") as f:
            config_data = json.loads(f.read())
    else:
        config_data = {
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
    return config_data


def validate_config_settings(config):
    "Make sure relvant enviorment variables are set"
    if config.get("github_app", {}).get("check_signature", False):
        if not os.environ.get("GITHUB_APP_WEBHOOK_SECRET"):
            raise EnvironmentError(
                "The environment variable 'GITHUB_APP_WEBHOOK_SECRET' is not set."
            )

    if config.get("language_model", {}).get("provider", {}) == "litellm":
        if config.get("language_model", {}).get("enable_observability_logging", False):
            if not os.environ.get("SUPABASE_URL"):
                raise EnvironmentError(
                    "The environment variable 'SUPABASE_URL' is not set."
                )
            if not os.environ.get("SUPABASE_KEY"):
                raise EnvironmentError(
                    "The environment variable 'SUPABASE_KEY' is not set."
                )
    return config


CONFIG_DATA = validate_config_settings(get_config())
