import click


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
