import os
import pytest
from unittest import mock
from kaizen.helpers.output import create_folder

# Mock logger
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

def test_create_new_folder_when_not_exists(mock_os_path_exists, mock_os_makedirs, mock_logger_debug):
    folder_path = 'new_folder'
    mock_os_path_exists.return_value = False

    create_folder(folder_path)

    mock_os_path_exists.assert_called_once_with(folder_path)
    mock_os_makedirs.assert_called_once_with(folder_path)
    mock_logger_debug.assert_called_once_with(f"Folder '{folder_path}' created successfully.")

def test_do_nothing_when_folder_already_exists(mock_os_path_exists, mock_os_makedirs, mock_logger_debug):
    folder_path = 'existing_folder'
    mock_os_path_exists.return_value = True

    create_folder(folder_path)

    mock_os_path_exists.assert_called_once_with(folder_path)
    mock_os_makedirs.assert_not_called()
    mock_logger_debug.assert_called_once_with(f"Folder '{folder_path}' already exists.")

def test_raise_value_error_when_folder_path_is_empty():
    with pytest.raises(ValueError, match="Folder path cannot be empty"):
        create_folder('')

def test_create_deeply_nested_folder(mock_os_path_exists, mock_os_makedirs, mock_logger_debug):
    folder_path = 'a/b/c/d/e/f/g'
    mock_os_path_exists.return_value = False

    create_folder(folder_path)

    mock_os_path_exists.assert_called_once_with(folder_path)
    mock_os_makedirs.assert_called_once_with(folder_path)
    mock_logger_debug.assert_called_once_with(f"Folder '{folder_path}' created successfully.")

def test_create_folder_with_special_characters(mock_os_path_exists, mock_os_makedirs, mock_logger_debug):
    folder_path = 'folder_with_special_!@#$%^&*()'
    mock_os_path_exists.return_value = False

    create_folder(folder_path)

    mock_os_path_exists.assert_called_once_with(folder_path)
    mock_os_makedirs.assert_called_once_with(folder_path)
    mock_logger_debug.assert_called_once_with(f"Folder '{folder_path}' created successfully.")

def test_create_folder_with_max_path_length(mock_os_path_exists, mock_os_makedirs, mock_logger_debug):
    # Adjusting the max path length to a more typical value for modern filesystems
    max_path_length = os.pathconf('/', 'PC_PATH_MAX')
    folder_path = 'a' * max_path_length
    mock_os_path_exists.return_value = False

    create_folder(folder_path)

    mock_os_path_exists.assert_called_once_with(folder_path)
    mock_os_makedirs.assert_called_once_with(folder_path)
    mock_logger_debug.assert_called_once_with(f"Folder '{folder_path}' created successfully.")

def test_create_folder_with_invalid_characters(mock_os_path_exists, mock_os_makedirs, mock_logger_debug):
    # Assuming the filesystem does not allow characters like ':', '*', '?', '<', '>', '|'
    invalid_characters = [':', '*', '?', '<', '>', '|']
    for char in invalid_characters:
        folder_path = f'invalid{char}folder'
        mock_os_path_exists.return_value = False

        with pytest.raises(OSError):
            create_folder(folder_path)

        mock_os_path_exists.assert_called_once_with(folder_path)
        mock_os_makedirs.assert_not_called()
        mock_logger_debug.assert_not_called()