import click
from kaizen.generator.unit_test import UnitTestGenerator
from kaizen.actors.unit_test_runner import UnitTestRunner


@click.group()
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
    runner = UnitTestRunner()
    test_results = runner.discover_and_run_tests(test_file=file_path)
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
