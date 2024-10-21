import logging
import pytest

# Assuming the function is in the module kaizen/llms/provider.py
from kaizen.llms.provider import set_all_loggers_to_ERROR


@pytest.fixture
def setup_loggers():
    # Setup: Create some loggers with different levels
    loggers = {
        "logger1": logging.getLogger("logger1"),
        "logger2": logging.getLogger("logger2"),
        "logger3": logging.getLogger("logger3"),
    }
    loggers["logger1"].setLevel(logging.DEBUG)
    loggers["logger2"].setLevel(logging.INFO)
    loggers["logger3"].setLevel(logging.WARNING)

    yield loggers

    # Teardown: Reset loggers to default level (WARNING)
    for logger in loggers.values():
        logger.setLevel(logging.WARNING)


def test_set_all_loggers_to_ERROR(setup_loggers):
    # Test: Verify all existing loggers are set to ERROR level
    set_all_loggers_to_ERROR()

    for name, logger in setup_loggers.items():
        assert logger.level == logging.ERROR, f"Logger {name} not set to ERROR level"


def test_no_loggers_present(monkeypatch):
    # Edge Case: Handle scenario where no loggers are present
    # Mock the loggerDict to simulate no loggers
    monkeypatch.setattr(logging.Logger.manager, "loggerDict", {})

    set_all_loggers_to_ERROR()

    # Verify no errors occur and loggerDict is still empty
    assert logging.Logger.manager.loggerDict == {}, "LoggerDict should be empty"
