import click
from kaizen.generator.pr_description import PRDescriptionGenerator
from kaizen.llms.provider import LLMProvider
from ..config.manager import load_config


@click.group()
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


@click.command()
@click.argument("diff", type=str, required=True)
def generate_commit_msg(diff):
    """Generate a commit message based on the provided diff"""
    model_config = load_config()["language_model"]["models"][0]["litellm_params"]
    generator = PRDescriptionGenerator(LLMProvider(model_config=model_config))
    desc = generator.generate_pull_request_desc(
        diff_text=diff,
        pull_request_title="",
        pull_request_desc="",
        pull_request_files=[],
        user="",
    )
    msg, _, _ = generator.generate_pr_commit_message(desc)
    click.echo(f'{msg["subject"]}\n\n{msg["body"]}')
