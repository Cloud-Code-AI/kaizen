import pytest
import os

if __name__ == "__main__":
    test_dir = ".kaizen/tests"
    pytest.main(["-v", test_dir])