import click
import os
import json
from kaizen.generator.e2e_tests import E2ETestGenerator
from kaizen.generator.unit_test import UnitTestGenerator

CONFIG_FILE = os.path.expanduser("~/.myapp_config.json")

# Default configuration
DEFAULT_CONFIG = {"region": "us-east-1", "output": "json", "timeout": 60}


def load_config():
    config = DEFAULT_CONFIG.copy()  # Start with default config
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                user_config = json.load(f)
            config.update(user_config)  # Override defaults with user config
        except json.JSONDecodeError:
            click.echo(
                f"Warning: Config file {CONFIG_FILE} is not valid JSON. Using default configuration."
            )
        except IOError as e:
            click.echo(
                f"Warning: Unable to read config file {CONFIG_FILE}. Using default configuration. Error: {e}"
            )
    return config


def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        click.echo(f"Error: Unable to save config file {CONFIG_FILE}. Error: {e}")


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
    E2ETestGenerator().generate_e2e_tests(url)


@cli.group()
def unit_test():
    """Unit test command group"""
    pass


@unit_test.command()
@click.argument("file_path", required=True)
@click.option("--output-folder", default=None)
@click.option("--enable-critique", is_flag=True, default=False)
@click.option("--verbose", is_flag=True, default=False)
@click.option("--max-critique", default=1, type=int)
def generate(file_path, output_folder, enable_critique, verbose, max_critique):
    """Generate unit tests for a file"""
    generator = UnitTestGenerator()
    generator.generate_tests(
        file_path=file_path,
        output_path=output_folder,
        enable_critique=enable_critique,
        verbose=verbose,
        max_critique=max_critique,
    )


@unit_test.command()
@click.argument("dir_path", required=True)
@click.option("--output-folder", default=None)
@click.option("--enable-critique", is_flag=True, default=False)
@click.option("--verbose", is_flag=True, default=False)
@click.option("--max-critique", default=1, type=int)
def generate_dir(dir_path, output_folder, enable_critique, verbose, max_critique):
    """Generate unit tests for a directory"""
    generator = UnitTestGenerator()
    result = generator.generate_tests_from_dir(
        dir_path=dir_path,
        output_path=output_folder,
        enable_critique=enable_critique,
        verbose=verbose,
        max_critique=max_critique,
    )
    click.echo(result)


@unit_test.command()
@click.option("--file-path", default=None)
def run_tests(file_path):
    """Run unit tests"""
    generator = UnitTestGenerator()
    test_results = generator.run_tests(file_path=file_path)
    for file_path, result in test_results.items():
        click.echo(f"Results for {file_path}:")
        if "error" in result:
            click.echo(f"  Error: {result['error']}")
        else:
            click.echo(f"  Tests run: {result.get('tests_run', 'N/A')}")
            click.echo(f"  Failures: {result.get('failures', 'N/A')}")
            click.echo(f"  Errors: {result.get('errors', 'N/A')}")
        click.echo()


@unit_test.command()
@click.argument("code", required=True)
@click.option("--file-path", default="sample.py")
def generate_from_code(code, file_path):
    """Generate unit tests from provided code"""
    generator = UnitTestGenerator()
    generator.generate_tests(file_path=file_path, content=code)


@cli.group()
def reviewer():
    """reviewer command group"""
    pass


@reviewer.command()
@click.argument("github_url", required=True)
@click.argument("branch", required=True)
def work(github_url, branch):
    """Run reviewer work"""
    click.echo(f"Reviewing {github_url} on branch {branch}")
    # Implement the reviewer work logic here


if __name__ == "__main__":
    cli()
