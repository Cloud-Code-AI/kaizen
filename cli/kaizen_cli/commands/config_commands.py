import click
import json
from ..config.manager import (
    save_config,
    get_nested,
    is_valid_key,
    set_nested,
)
from ..config.default_config import DEFAULT_CONFIG


@click.group()
def config():
    pass


@config.command()
@click.argument("key", nargs=-1)
@click.argument("value", required=False)
@click.pass_obj
def config_setup(obj, key, value):
    """Get or set a configuration value."""
    if not key:
        click.echo(json.dumps(obj, indent=2))
        return

    if not is_valid_key(DEFAULT_CONFIG, key):
        click.echo(f"Invalid config key: {'.'.join(key)}")
        return

    if value is None:
        # Get the value
        result = get_nested(obj, key)
        click.echo(f"{'.'.join(key)}: {json.dumps(result, indent=2)}")
    else:
        # Set the value
        try:
            # Try to parse the value as JSON
            parsed_value = json.loads(value)
        except json.JSONDecodeError:
            # If it's not valid JSON, treat it as a string
            parsed_value = value

        set_nested(obj, key, parsed_value)
        save_config(obj)
        click.echo(f"Updated {'.'.join(key)} to {parsed_value}")


@config.command()
@click.pass_obj
def show(obj):
    """Show the current configuration."""
    click.echo(json.dumps(obj, indent=2))


@config.command()
@click.option("--name", required=True, help="Name of the model")
@click.option("--model", required=True, help="LiteLLM model identifier")
@click.option("--api-key", required=False, help="API key for the model", default=None)
@click.option(
    "--api-base", required=False, help="API base URL for the model", default=None
)
@click.pass_obj
def add_model(obj, name, model, api_key, api_base):
    """Add or replace a model in the configuration."""
    new_model = {
        "model_name": name,
        "litellm_params": {"model": model, "api_key": api_key, "api_base": api_base},
    }

    models = get_nested(obj, ("language_model", "models"))
    for i, existing_model in enumerate(models):
        if existing_model["model_name"] == name:
            models[i] = new_model
            break
    else:
        models.append(new_model)

    set_nested(obj, ("language_model", "models"), models)
    save_config(obj)
    click.echo(f"Model '{name}' has been added/updated in the configuration.")


@config.command()
@click.argument("api_key", required=True)
@click.pass_obj
def add_api_key(obj, api_key):
    """Update the Kaizen API key."""
    set_nested(obj, ("kaizen_api_key",), api_key)
    save_config(obj)
    click.echo("Kaizen API key has been updated.")


@config.command()
@click.argument("name", required=True)
@click.pass_obj
def delete_model(obj, name):
    """Delete a model from the configuration."""
    models = get_nested(obj, ("language_model", "models"))
    original_length = len(models)

    models = [model for model in models if model["model_name"] != name]

    if len(models) == original_length:
        click.echo(f"Model '{name}' not found in the configuration.")
    else:
        set_nested(obj, ("language_model", "models"), models)
        save_config(obj)
        click.echo(f"Model '{name}' has been deleted from the configuration.")
