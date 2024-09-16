import click
from .config.manager import load_config
from .commands.config_commands import config
from .commands.unit_test_commands import unit_test
from .commands.reviewer_commands import reviewer
from kaizen.generator.e2e_tests import E2ETestGenerator


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = load_config()


@cli.command()
@click.argument("url", required=True)
def ui_tests(url):
    """Run ui test generation"""
    E2ETestGenerator().generate_e2e_tests(url)


# Add command groups
cli.add_command(config)
cli.add_command(unit_test)
cli.add_command(reviewer)

if __name__ == "__main__":
    cli()
