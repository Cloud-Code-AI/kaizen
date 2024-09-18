import os
import json
from .default_config import DEFAULT_CONFIG
from ..utils import deep_update, set_nested

CONFIG_FILE = os.path.expanduser("~/.kaizen_config.json")


def load_config():
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                user_config = json.load(f)
            config = deep_update(config, user_config)
        except json.JSONDecodeError:
            print(
                f"Warning: Config file {CONFIG_FILE} is not valid JSON. Using default configuration."
            )
        except IOError as e:
            print(
                f"Warning: Unable to read config file {CONFIG_FILE}. Using default configuration. Error: {e}"
            )

    # Override with environment variables
    for key, value in os.environ.items():
        if key.startswith("KAIZEN_"):
            config_key = key[6:].lower().split("__")
            try:
                parsed_value = json.loads(value)
            except json.JSONDecodeError:
                parsed_value = value
            set_nested(config, config_key, parsed_value)

    return config


def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"Error: Unable to save config file {CONFIG_FILE}. Error: {e}")


def get_nested(data, keys):
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        else:
            return None
    return data


def is_valid_key(config, keys):
    current = config
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return False
    return True
