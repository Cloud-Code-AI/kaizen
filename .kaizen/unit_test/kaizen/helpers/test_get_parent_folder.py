# File: test_get_parent_folder.py

import os
import pytest
from unittest.mock import patch

# Assuming the function is located in kaizen/helpers/output.py
from kaizen.helpers.output import get_parent_folder

@pytest.fixture
def mock_getcwd():
    with patch('os.getcwd') as mock:
        yield mock

@pytest.mark.parametrize("mock_return_value, expected", [
    ('/home/user/project', '/home/user/project'),
    ('/', '/'),
    ('', '')
])
def test_get_parent_folder_normal_and_edge_cases(mock_getcwd, mock_return_value, expected):
    mock_getcwd.return_value = mock_return_value
    assert get_parent_folder() == expected

def test_get_parent_folder_oserror(mock_getcwd):
    mock_getcwd.side_effect = OSError('Unable to get current working directory')
    with pytest.raises(OSError, match='Unable to get current working directory'):
        get_parent_folder()