import click
import os
import json
from kaizen.generator.ui import UITestGenerator

CONFIG_FILE = os.path.expanduser("~/.myapp_config.json")

# Default configuration
DEFAULT_CONFIG = {"region": "us-east-1", "output": "json", "timeout": 60}


def load_config():
    config = DEFAULT_CONFIG.copy()  # Start with default config
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            user_config = json.load(f)
        config.update(user_config)  # Override defaults with user config
    return config


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = load_config()


@cli.command()
@click.option("--key", prompt="Config key")
@click.option("--value", prompt="Config value")
@click.pass_obj
def config(obj, key, value):
    """Set a configuration value."""
    if key in DEFAULT_CONFIG:
        obj[key] = type(DEFAULT_CONFIG[key])(
            value
        )  # Convert to the same type as in DEFAULT_CONFIG
        save_config({k: v for k, v in obj.items() if k in DEFAULT_CONFIG})
        click.echo(f"Updated {key} to {value}")
    else:
        click.echo(
            f"Invalid config key. Valid keys are: {', '.join(DEFAULT_CONFIG.keys())}"
        )


@cli.command()
@click.pass_obj
def show_config(obj):
    """Show the current configuration."""
    for key, value in obj.items():
        click.echo(f"{key}: {value}")


@cli.command()
@click.argument("command")
@click.option("--region", default=None)
@click.pass_obj
def run(obj, command, region):
    """Run a command with the stored configuration."""
    region = region or obj["region"]
    click.echo(f"Running {command} in region {region} with timeout {obj['timeout']}s")


@cli.command()
@click.argument("url", required=True)
def ui_tests(url):
    """Run ui test generation"""
    UITestGenerator().generate_ui_tests(url)


@cli.group()
def reviewer():
    """reviewer command group"""
    pass


@reviewer.command()
@click.argument("github_url", required=True)
@click.argument("branch", required=True)
def work(url):
    """Run ui test generation"""
    UITestGenerator().generate_ui_tests(url)


if __name__ == "__main__":
    cli()
