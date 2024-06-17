import click
from kaizen.generator.ui import UITestGenerator


@click.group()
def cli():
    """Kaizen CLI"""
    pass


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
