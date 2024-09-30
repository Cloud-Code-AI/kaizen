import logging
import pytest
from unittest.mock import patch

# Import the function to be tested
from kaizen.llms.provider import set_all_loggers_to_ERROR

@pytest.fixture
def setup_loggers():
    # Setup a test environment with mock loggers
    logger_names = ['test_logger_1', 'test_logger_2', 'test_placeholder']
    loggers = {}
    
    for name in logger_names:
        if name == 'test_placeholder':
            loggers[name] = logging.PlaceHolder(name)
        else:
            loggers[name] = logging.getLogger(name)
            loggers[name].setLevel(logging.INFO)  # Set initial level to INFO
    
    return loggers

def test_set_all_loggers_to_ERROR(setup_loggers):
    with patch.dict(logging.Logger.manager.loggerDict, setup_loggers, clear=True):
        set_all_loggers_to_ERROR()
        
        # Verify that all actual loggers are set to ERROR level
        for name, logger in setup_loggers.items():
            if isinstance(logger, logging.Logger):
                assert logger.level == logging.ERROR, f"Logger {name} was not set to ERROR level"
            else:
                # Ensure PlaceHolder objects are not modified
                assert isinstance(logger, logging.PlaceHolder), f"{name} should be a PlaceHolder"

# Run the tests using pytest
if __name__ == "__main__":
    pytest.main()