import pytest
from unittest.mock import patch, AsyncMock
from kaizen.helpers.output import get_web_html
from bs4 import BeautifulSoup

@pytest.fixture
@patch('kaizen.helpers.output.get_html', new_callable=AsyncMock)
def mock_get_html(mock_get_html):
    return mock_get_html

@patch('kaizen.helpers.output.nest_asyncio.apply')
def test_get_web_html_normal_case(mock_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    mock_get_html.return_value = '<html><body><svg></svg><p>Hello World</p><!-- Comment --><style>body{color: red;}</style></body></html>'
    expected_html = '<html>\n <body>\n  <p>\n   Hello World\n  </p>\n </body>\n</html>'

    result = get_web_html(url)
    assert result == expected_html
    mock_apply.assert_called_once()
    mock_get_html.assert_awaited_once_with(url)

@patch('kaizen.helpers.output.nest_asyncio.apply')
def test_get_web_html_no_svg_no_comments_no_style(mock_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    mock_get_html.return_value = '<html><body><p>Hello World</p></body></html>'
    expected_html = '<html>\n <body>\n  <p>\n   Hello World\n  </p>\n </body>\n</html>'

    result = get_web_html(url)
    assert result == expected_html
    mock_apply.assert_called_once()
    mock_get_html.assert_awaited_once_with(url)

@patch('kaizen.helpers.output.nest_asyncio.apply')
def test_get_web_html_only_svg(mock_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    mock_get_html.return_value = '<html><body><svg></svg></body></html>'
    expected_html = '<html>\n <body>\n </body>\n</html>'

    result = get_web_html(url)
    assert result == expected_html
    mock_apply.assert_called_once()
    mock_get_html.assert_awaited_once_with(url)

@patch('kaizen.helpers.output.nest_asyncio.apply')
def test_get_web_html_only_comments(mock_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    mock_get_html.return_value = '<html><body><!-- Comment --></body></html>'
    expected_html = '<html>\n <body>\n </body>\n</html>'

    result = get_web_html(url)
    assert result == expected_html
    mock_apply.assert_called_once()
    mock_get_html.assert_awaited_once_with(url)

@patch('kaizen.helpers.output.nest_asyncio.apply')
def test_get_web_html_only_style(mock_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    mock_get_html.return_value = '<html><body><style>body{color: red;}</style></body></html>'
    expected_html = '<html>\n <body>\n </body>\n</html>'

    result = get_web_html(url)
    assert result == expected_html
    mock_apply.assert_called_once()
    mock_get_html.assert_awaited_once_with(url)

@patch('kaizen.helpers.output.nest_asyncio.apply')
def test_get_web_html_empty_html(mock_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    mock_get_html.return_value = ''
    expected_html = ''

    result = get_web_html(url)
    assert result == expected_html
    mock_apply.assert_called_once()
    mock_get_html.assert_awaited_once_with(url)

@patch('kaizen.helpers.output.nest_asyncio.apply')
def test_get_web_html_invalid_html(mock_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    mock_get_html.return_value = '<html><body><svg></svg><p>Hello World</p><!-- Comment --><style>body{color: red;}</style></body></html>'
    expected_html = '<html>\n <body>\n  <p>\n   Hello World\n  </p>\n </body>\n</html>'

    result = get_web_html(url)
    assert result == expected_html
    mock_apply.assert_called_once()
    mock_get_html.assert_awaited_once_with(url)

@patch('kaizen.helpers.output.nest_asyncio.apply')
def test_get_web_html_error_handling(mock_apply, mock_get_html):
    url = 'https://cloudcode.ai'
    mock_get_html.side_effect = Exception('Network error')

    with pytest.raises(Exception, match='Network error'):
        get_web_html(url)
    mock_apply.assert_called_once()
    mock_get_html.assert_awaited_once_with(url)