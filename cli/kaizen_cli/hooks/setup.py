import os
import shutil
import click

HOOK_TYPES = ["prepare-commit-msg"]


@click.group()
def hooks():
    """Manage git hooks"""
    pass


@hooks.command()
@click.argument("hook_type", type=click.Choice(HOOK_TYPES))
def install(hook_type):
    """Install a specific git hook"""
    source = os.path.join(os.path.dirname(__file__), hook_type)
    print(source)
    destination = os.path.join(".git", "hooks", hook_type)

    if not os.path.exists(source):
        click.echo(f"Error: Hook script for {hook_type} not found.")
        return

    try:
        # Create the destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy(source, destination)
        os.chmod(destination, 0o755)
        click.echo(f"{hook_type} hook installed successfully")
    except IOError as e:
        click.echo(f"Error installing {hook_type} hook: {str(e)}")


@hooks.command()
def install_all():
    """Install all available git hooks"""
    for hook_type in HOOK_TYPES:
        ctx = click.get_current_context()
        ctx.invoke(install, hook_type=hook_type)


@hooks.command()
@click.argument("hook_type", type=click.Choice(HOOK_TYPES))
def uninstall(hook_type):
    """Uninstall a specific git hook"""
    hook_path = os.path.join(".git", "hooks", hook_type)
    if os.path.exists(hook_path):
        os.remove(hook_path)
        click.echo(f"{hook_type} hook uninstalled successfully")
    else:
        click.echo(f"{hook_type} hook not found")


@hooks.command()
def uninstall_all():
    """Uninstall all git hooks"""
    for hook_type in HOOK_TYPES:
        ctx = click.get_current_context()
        ctx.invoke(uninstall, hook_type=hook_type)
