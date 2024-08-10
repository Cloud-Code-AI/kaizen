import pytest
import os
from unittest import mock
from kaizen.helpers.output import create_folder

# Mock logger to avoid actual logging during tests
logger = mock.Mock()

@pytest.fixture
def mock_os_path_exists():
    with mock.patch('os.path.exists') as mock_exists:
        yield mock_exists

@pytest.fixture
def mock_os_makedirs():
    with mock.patch('os.makedirs') as mock_makedirs:
        yield mock_makedirs

@pytest.fixture
def mock_logger_debug():
    with mock.patch('kaizen.helpers.output.logger.debug') as mock_debug:
        yield mock_debug

def test_create_folder_successful_creation(mock_os_path_exists, mock_os_makedirs, mock_logger_debug):
    folder_path = "/some/new/folder"
    mock_os_path_exists.return_value = False

    create_folder(folder_path)

    mock_os_path_exists.assert_called_once_with(folder_path)
    mock_os_makedirs.assert_called_once_with(folder_path)
    mock_logger_debug.assert_called_once_with(f"Folder '{folder_path}' created successfully.")

def test_create_folder_already_exists(mock_os_path_exists, mock_os_makedirs, mock_logger_debug):
    folder_path = "/some/existing/folder"
    mock_os_path_exists.return_value = True

    create_folder(folder_path)

    mock_os_path_exists.assert_called_once_with(folder_path)
    mock_os_makedirs.assert_not_called()
    mock_logger_debug.assert_called_once_with(f"Folder '{folder_path}' already exists.")

def test_create_folder_empty_path():
    with pytest.raises(ValueError, match="Folder path cannot be empty"):
        create_folder("")

def test_create_folder_none_path():
    with pytest.raises(ValueError, match="Folder path cannot be empty"):
        create_folder(None)