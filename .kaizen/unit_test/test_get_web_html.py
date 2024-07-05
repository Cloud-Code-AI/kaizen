import pytest
from unittest.mock import patch, AsyncMock
from kaizen.helpers.output import get_web_html
from bs4 import BeautifulSoup
import asyncio


@pytest.mark.asyncio
@patch("kaizen.helpers.output.get_html", new_callable=AsyncMock)
@patch("kaizen.helpers.output.nest_asyncio.apply")
def test_get_web_html_normal_case(mock_nest_asyncio, mock_get_html):
    mock_get_html.return_value = "<html><body><svg></svg><p>Hello World!</p><style>.test{}</style><!-- Comment --></body></html>"
    url = "https://cloudcode.ai"
    result = asyncio.run(get_web_html(url))
    expected_html = BeautifulSoup(
        "<html><body><p>Hello World!</p></body></html>", "html.parser"
    ).prettify()
    assert result == expected_html


@pytest.mark.asyncio
@patch("kaizen.helpers.output.get_html", new_callable=AsyncMock)
@patch("kaizen.helpers.output.nest_asyncio.apply")
def test_get_web_html_no_svg_no_comments_no_style(mock_nest_asyncio, mock_get_html):
    mock_get_html.return_value = "<html><body><p>Hello World!</p></body></html>"
    url = "https://cloudcode.ai"
    result = asyncio.run(get_web_html(url))
    expected_html = BeautifulSoup(
        "<html><body><p>Hello World!</p></body></html>", "html.parser"
    ).prettify()
    assert result == expected_html


@pytest.mark.asyncio
@patch("kaizen.helpers.output.get_html", new_callable=AsyncMock)
@patch("kaizen.helpers.output.nest_asyncio.apply")
def test_get_web_html_only_svg(mock_nest_asyncio, mock_get_html):
    mock_get_html.return_value = "<html><body><svg></svg></body></html>"
    url = "https://cloudcode.ai"
    result = asyncio.run(get_web_html(url))
    expected_html = BeautifulSoup(
        "<html><body></body></html>", "html.parser"
    ).prettify()
    assert result == expected_html


@pytest.mark.asyncio
@patch("kaizen.helpers.output.get_html", new_callable=AsyncMock)
@patch("kaizen.helpers.output.nest_asyncio.apply")
def test_get_web_html_only_comments(mock_nest_asyncio, mock_get_html):
    mock_get_html.return_value = "<html><body><!-- Comment --></body></html>"
    url = "https://cloudcode.ai"
    result = asyncio.run(get_web_html(url))
    expected_html = BeautifulSoup(
        "<html><body></body></html>", "html.parser"
    ).prettify()
    assert result == expected_html


@pytest.mark.asyncio
@patch("kaizen.helpers.output.get_html", new_callable=AsyncMock)
@patch("kaizen.helpers.output.nest_asyncio.apply")
def test_get_web_html_only_style(mock_nest_asyncio, mock_get_html):
    mock_get_html.return_value = "<html><body><style>.test{}</style></body></html>"
    url = "https://cloudcode.ai"
    result = asyncio.run(get_web_html(url))
    expected_html = BeautifulSoup(
        "<html><body></body></html>", "html.parser"
    ).prettify()
    assert result == expected_html


@pytest.mark.asyncio
@patch("kaizen.helpers.output.get_html", new_callable=AsyncMock)
@patch("kaizen.helpers.output.nest_asyncio.apply")
def test_get_web_html_empty_html(mock_nest_asyncio, mock_get_html):
    mock_get_html.return_value = ""
    url = "https://cloudcode.ai"
    result = asyncio.run(get_web_html(url))
    expected_html = BeautifulSoup("", "html.parser").prettify()
    assert result == expected_html


@pytest.mark.asyncio
@patch("kaizen.helpers.output.get_html", new_callable=AsyncMock)
@patch("kaizen.helpers.output.nest_asyncio.apply")
def test_get_web_html_invalid_html(mock_nest_asyncio, mock_get_html):
    mock_get_html.return_value = "<html><body><svg></svg><p>Hello World!</p><style>.test{}</style><!-- Comment --></body></html>"
    url = "invalid_url"
    with pytest.raises(Exception):
        asyncio.run(get_web_html(url))
