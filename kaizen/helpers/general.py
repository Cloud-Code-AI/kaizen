import re
import time
from functools import wraps
from pathlib import Path


def safe_path_join(base_path, *paths):
    """
    Safely join two or more pathname components.

    Args:
    base_path (str): The base path.
    *paths (str): Additional path components to join.

    Returns:
    Path: The safely joined path.

    Raises:
    ValueError: If the resulting path would be outside the base path.
    """
    base = Path(base_path).resolve()
    full_path = (base.joinpath(*paths)).resolve()

    if base not in full_path.parents:
        raise ValueError("Resulting path would be outside the base path.")

    return full_path


def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    print(
                        f"Attempt {attempts} failed: error |{e}|. Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)

        return wrapper

    return decorator


def clean_python_code(code):
    match = re.search(r"```(?:python)?\n(.*)\n```", code, re.DOTALL)
    if match:
        return match.group(1)
    return None
