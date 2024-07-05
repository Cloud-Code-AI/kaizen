import pytest
from unittest import mock
from kaizen.helpers.output import create_folder


@mock.patch("kaizen.helpers.output.os.makedirs")
@mock.patch("kaizen.helpers.output.os.path.exists")
@mock.patch("kaizen.helpers.output.logger")
def test_create_folder_success(mock_logger, mock_exists, mock_makedirs):
    folder_path = "/fake/path"
    mock_exists.return_value = False

    create_folder(folder_path)

    mock_exists.assert_called_once_with(folder_path)
    mock_makedirs.assert_called_once_with(folder_path)
    mock_logger.debug.assert_called_once_with(
        f"Folder '{folder_path}' created successfully."
    )


@mock.patch("kaizen.helpers.output.os.makedirs")
@mock.patch("kaizen.helpers.output.os.path.exists")
@mock.patch("kaizen.helpers.output.logger")
def test_create_folder_already_exists(mock_logger, mock_exists, mock_makedirs):
    folder_path = "/fake/path"
    mock_exists.return_value = True

    create_folder(folder_path)

    mock_exists.assert_called_once_with(folder_path)
    mock_makedirs.assert_not_called()
    mock_logger.debug.assert_called_once_with(f"Folder '{folder_path}' already exists.")


@mock.patch("kaizen.helpers.output.os.makedirs")
@mock.patch("kaizen.helpers.output.os.path.exists")
@mock.patch("kaizen.helpers.output.logger")
def test_create_folder_os_error(mock_logger, mock_exists, mock_makedirs):
    folder_path = "/fake/path"
    mock_exists.return_value = False
    mock_makedirs.side_effect = OSError("Permission denied")

    with pytest.raises(OSError, match="Permission denied"):
        create_folder(folder_path)

    mock_exists.assert_called_once_with(folder_path)
    mock_makedirs.assert_called_once_with(folder_path)
    mock_logger.debug.assert_not_called()


@mock.patch("kaizen.helpers.output.os.makedirs")
@mock.patch("kaizen.helpers.output.os.path.exists")
@mock.patch("kaizen.helpers.output.logger")
def test_create_folder_empty_path(mock_logger, mock_exists, mock_makedirs):
    folder_path = ""
    mock_exists.return_value = False

    with pytest.raises(ValueError, match="Folder path cannot be empty"):
        create_folder(folder_path)

    mock_exists.assert_not_called()
    mock_makedirs.assert_not_called()
    mock_logger.debug.assert_not_called()
