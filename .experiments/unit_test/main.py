import os
import shutil
import tempfile
from github import Github
from git import Repo
from kaizen.generator.unit_test import UnitTestGenerator


def run_unit_tests_for_repos(github_token, repos_and_files):
    generator = UnitTestGenerator(verbose=True)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_output_dir = os.path.join(current_dir, "output")
    if github_token:
        g = Github(github_token)
    else:
        g = Github()

    for repo_url, file_list in repos_and_files.items():
        repo_name = repo_url.split("/")[-1].replace(".git", "")
        print(f"\nProcessing repository: {repo_name}")

        with tempfile.TemporaryDirectory() as temp_dir:
            # Clone the repository
            print(f"Cloning {repo_url} to {temp_dir}")
            github_repo = g.get_repo(
                "/".join(repo_url.split("/")[-2:]).replace(".git", "")
            )
            Repo.clone_from(github_repo.clone_url, temp_dir)

            # Create an interim folder for generated tests
            # current_dir = os.path.dirname(os.path.abspath(__file__))
            interim_dir = os.path.join(current_dir, "interim_tests")
            os.makedirs(interim_dir, exist_ok=True)

            # Generate and run tests
            successful_tests = []
            failed_tests = []

            for file_path in file_list:
                full_path = os.path.join(temp_dir, file_path)
                if not os.path.exists(full_path):
                    print(f"File not found: {file_path}")
                    continue

                print(f"Generating tests for: {file_path}")
                try:
                    test_files, total_usage = generator.generate_tests(
                        file_path=full_path,
                        enable_critique=True,
                        verbose=True,
                        max_critique=1,
                        output_path=interim_dir,
                        temp_dir=interim_dir,  # Store generated tests in the interim folder
                    )
                    print(f"Generated tests: {test_files}")
                except Exception as e:
                    print(f"Error generating tests for {file_path}: {str(e)}")
                    failed_tests.append(file_path)
                    continue

            # Run all generated tests
            print("\nRunning all generated tests:")
            for test_file in test_files:
                test_results = generator.run_tests(
                    test_file
                )  # Run tests from the interim folder

                # Process test results
                for file_path, result in test_results.items():
                    relative_path = os.path.relpath(file_path, interim_dir)
                    if (
                        "error" in result
                        or result.get("failures", 0) > 0
                        or result.get("errors", 0) > 0
                    ):
                        failed_tests.append(relative_path)
                    else:
                        successful_tests.append(relative_path)

                    print(f"\nResults for {relative_path}:")
                    if "error" in result:
                        print(f"  Error: {result['error']}")
                    else:
                        print(f"  Tests run: {result.get('tests_run', 'N/A')}")
                        print(f"  Failures: {result.get('failures', 'N/A')}")
                        print(f"  Errors: {result.get('errors', 'N/A')}")

            # Copy generated test files from interim folder to output directories
            repo_output_dir = os.path.join(base_output_dir, repo_name)
            successful_dir = os.path.join(repo_output_dir, "successful")
            failed_dir = os.path.join(repo_output_dir, "failed")

            os.makedirs(successful_dir, exist_ok=True)
            os.makedirs(failed_dir, exist_ok=True)

            for file_path in successful_tests:
                src = os.path.join(interim_dir, file_path)
                dst = os.path.join(successful_dir, file_path)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                else:
                    print(f"Warning: Source file not found: {src}")

            for file_path in failed_tests:
                src = os.path.join(interim_dir, file_path)
                dst = os.path.join(failed_dir, file_path)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                else:
                    print(f"Warning: Source file not found: {src}")

            print(f"\nProcessing complete for {repo_name}")
            print(f"Successful tests: {len(successful_tests)}")
            print(f"Failed tests: {len(failed_tests)}")


if __name__ == "__main__":
    # GitHub token for authentication
    github_token = None

    # Example usage
    repos_and_files = {
        "https://github.com/Cloud-Code-AI/kaizen.git": [
            "kaizen/reviewer/code_review.py",
            "kaizen/reviewer/code_scan.py",
        ],
        "https://github.com/Cloud-Code-AI/AkiraDocs.git": [
            "backend/app/analyze_repo.py"
        ],
    }

    run_unit_tests_for_repos(github_token, repos_and_files)
