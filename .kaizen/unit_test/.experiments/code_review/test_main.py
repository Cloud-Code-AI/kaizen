import os
import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from tqdm import tqdm

# Assuming the main function is in a file named main.py
from main import main

@pytest.fixture
def mock_process_pr():
    with patch('main.process_pr') as mock:
        yield mock

@pytest.fixture
def mock_save_review():
    with patch('main.save_review') as mock:
        yield mock

@pytest.fixture
def mock_logger():
    with patch('main.logger') as mock:
        yield mock

def test_multiple_pr_urls(mock_process_pr, mock_save_review, mock_logger):
    pr_urls = ['https://github.com/org/repo/pull/1', 'https://github.com/org/repo/pull/2']
    
    mock_process_pr.return_value = ('review_desc', 'comments', 'issues', 'combined_diff_data')

    with patch('os.makedirs'), \
         patch('os.path.join', return_value='/mock/path'), \
         patch('datetime.datetime') as mock_datetime:
        
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        
        main(pr_urls)

    assert mock_process_pr.call_count == 2
    assert mock_save_review.call_count == 2
    mock_logger.info.assert_called_with("All PRs processed successfully")

def test_empty_pr_urls(mock_process_pr, mock_save_review, mock_logger):
    pr_urls = []

    with patch('os.makedirs'), \
         patch('os.path.join', return_value='/mock/path'), \
         patch('datetime.datetime') as mock_datetime:
        
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        
        main(pr_urls)

    mock_process_pr.assert_not_called()
    mock_save_review.assert_not_called()
    mock_logger.info.assert_called_with("All PRs processed successfully")

def test_process_pr_exception(mock_process_pr, mock_save_review, mock_logger):
    pr_urls = ['https://github.com/org/repo/pull/1']
    
    mock_process_pr.side_effect = Exception("Simulated error")

    with patch('os.makedirs'), \
         patch('os.path.join', return_value='/mock/path'), \
         patch('datetime.datetime') as mock_datetime, \
         pytest.raises(Exception):
        
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        
        main(pr_urls)

    mock_process_pr.assert_called_once()
    mock_save_review.assert_not_called()
    mock_logger.info.assert_not_called_with("All PRs processed successfully")

@pytest.mark.parametrize("reeval_response", [True, False])
def test_reeval_response_flag(mock_process_pr, mock_save_review, mock_logger, reeval_response):
    pr_urls = ['https://github.com/org/repo/pull/1']
    
    mock_process_pr.return_value = ('review_desc', 'comments', 'issues', 'combined_diff_data')

    with patch('os.makedirs'), \
         patch('os.path.join', return_value='/mock/path'), \
         patch('datetime.datetime') as mock_datetime:
        
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, 0)
        
        main(pr_urls)

    mock_process_pr.assert_called_once_with(pr_urls[0], reeval_response=False)
    mock_save_review.assert_called_once()