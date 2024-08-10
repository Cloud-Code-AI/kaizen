import pytest
from unittest import mock
from kaizen.helpers.output import create_folder


@mock.patch("kaizen.helpers.output.os.makedirs")
@mock.patch("kaizen.helpers.output.os.path.exists")
@mock.patch("kaizen.helpers.output.logger")
def test_create_folder_success(mock_logger, mock_exists, mock_makedirs):
    mock_exists.return_value = False
    folder_path = "/path/to/folder"

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
    mock_exists.return_value = True
    folder_path = "/path/to/folder"

    create_folder(folder_path)

    mock_exists.assert_called_once_with(folder_path)
    mock_makedirs.assert_not_called()
    mock_logger.debug.assert_called_once_with(f"Folder '{folder_path}' already exists.")


@mock.patch("kaizen.helpers.output.os.makedirs")
@mock.patch("kaizen.helpers.output.os.path.exists")
@mock.patch("kaizen.helpers.output.logger")
def test_create_folder_empty_path(mock_logger, mock_exists, mock_makedirs):
    folder_path = ""

    with pytest.raises(ValueError) as excinfo:
        create_folder(folder_path)

    assert str(excinfo.value) == "Folder path cannot be empty"
    mock_exists.assert_not_called()
    mock_makedirs.assert_not_called()
    mock_logger.debug.assert_not_called()


@mock.patch("kaizen.helpers.output.os.makedirs")
@mock.patch("kaizen.helpers.output.os.path.exists")
@mock.patch("kaizen.helpers.output.logger")
def test_create_folder_none_path(mock_logger, mock_exists, mock_makedirs):
    folder_path = None

    with pytest.raises(ValueError) as excinfo:
        create_folder(folder_path)

    assert str(excinfo.value) == "Folder path cannot be empty"
    mock_exists.assert_not_called()
    mock_makedirs.assert_not_called()
    mock_logger.debug.assert_not_called()
