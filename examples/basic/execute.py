import pytest

if __name__ == "__main__":
    test_dir = ".kaizen/tests"
    pytest.main(["--timeout=60", "-v", test_dir, ])
