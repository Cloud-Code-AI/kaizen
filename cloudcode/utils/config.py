import json
import os


def get_config():
    with open("config.json", "r") as f:
        config_data = json.loads(f.read())
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
