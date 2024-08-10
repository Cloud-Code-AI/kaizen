import pytest
from unittest.mock import patch, AsyncMock
from bs4 import BeautifulSoup, Comment
import asyncio
import nest_asyncio
from kaizen.helpers.output import get_web_html

@pytest.fixture
def mock_get_html():
    with patch('kaizen.helpers.output.get_html', new_callable=AsyncMock) as mock:
        yield mock

@patch('nest_asyncio.apply')
def test_get_web_html_normal_case(mock_nest_asyncio_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    html_content = '''
    <html>
        <head><title>Test</title></head>
        <body>
            <svg></svg>
            <style>.test{color: red;}</style>
            <script>console.log('test');</script>
            <noscript>This is a noscript tag</noscript>
            <link rel="stylesheet" href="styles.css">
            <meta charset="UTF-8">
            <div>Content</div>
        </body>
    </html>
    '''
    mock_get_html.return_value = html_content

    result = get_web_html(url)

    soup = BeautifulSoup(result, 'html.parser')

    assert not soup.find_all('svg')
    assert not soup.find_all('style')
    assert not soup.find_all('script')
    assert not soup.find_all('noscript')
    assert not soup.find_all('link')
    assert not soup.find_all('meta')
    assert not soup.find_all('head')
    assert soup.find('div').text == 'Content'

@patch('nest_asyncio.apply')
def test_get_web_html_no_elements_to_remove(mock_nest_asyncio_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    html_content = '''
    <html>
        <body>
            <div>Content</div>
        </body>
    </html>
    '''
    mock_get_html.return_value = html_content

    result = get_web_html(url)

    soup = BeautifulSoup(result, 'html.parser')

    assert soup.find('div').text == 'Content'

@patch('nest_asyncio.apply')
def test_get_web_html_with_comments(mock_nest_asyncio_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    html_content = '''
    <html>
        <body>
            <!-- This is a comment -->
            <div>Content</div>
        </body>
    </html>
    '''
    mock_get_html.return_value = html_content

    result = get_web_html(url)

    soup = BeautifulSoup(result, 'html.parser')

    assert not soup.find_all(text=lambda text: isinstance(text, Comment))
    assert soup.find('div').text == 'Content'

@patch('nest_asyncio.apply')
def test_get_web_html_empty_html(mock_nest_asyncio_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    html_content = ''
    mock_get_html.return_value = html_content

    result = get_web_html(url)

    assert result == ''

@patch('nest_asyncio.apply')
def test_get_web_html_invalid_html(mock_nest_asyncio_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    html_content = '<html><div>Content</div>'  # Missing closing tags
    mock_get_html.return_value = html_content

    result = get_web_html(url)

    soup = BeautifulSoup(result, 'html.parser')

    assert soup.find('div').text == 'Content'

@patch('nest_asyncio.apply')
def test_get_web_html_error_handling(mock_nest_asyncio_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    mock_get_html.side_effect = Exception('Network error')

    with pytest.raises(Exception, match='Network error'):
        get_web_html(url)