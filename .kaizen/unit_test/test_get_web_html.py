import pytest
from unittest.mock import patch, AsyncMock
from bs4 import BeautifulSoup, Comment
import nest_asyncio
import asyncio
from kaizen.helpers.output import get_web_html


@pytest.fixture
async def mock_get_html():
    with patch("kaizen.helpers.output.get_html", new_callable=AsyncMock) as mock:
        yield mock


@patch("kaizen.helpers.output.nest_asyncio.apply")
@pytest.mark.asyncio
async def test_get_web_html_normal_case(mock_apply, mock_get_html):
    url = "https://cloudcode.ai"
    html_content = "<html><body><h1>Title</h1><svg></svg><style>body{}</style><!-- Comment --></body></html>"
    mock_get_html.return_value = html_content

    result = await get_web_html(url)

    assert "<svg>" not in result
    assert "<style>" not in result
    assert "<!-- Comment -->" not in result
    assert "<h1>Title</h1>" in result
    assert mock_apply.called
    mock_get_html.assert_called_once_with(url)


@patch("kaizen.helpers.output.nest_asyncio.apply")
@pytest.mark.asyncio
async def test_get_web_html_empty_html(mock_apply, mock_get_html):
    url = "https://cloudcode.ai"
    html_content = ""
    mock_get_html.return_value = html_content

    result = await get_web_html(url)

    assert result == ""
    assert mock_apply.called
    mock_get_html.assert_called_once_with(url)


@patch("kaizen.helpers.output.nest_asyncio.apply")
@pytest.mark.asyncio
async def test_get_web_html_no_svg_or_style(mock_apply, mock_get_html):
    url = "https://cloudcode.ai"
    html_content = "<html><body><h1>Title</h1></body></html>"
    mock_get_html.return_value = html_content

    result = await get_web_html(url)

    assert "<h1>Title</h1>" in result
    assert mock_apply.called
    mock_get_html.assert_called_once_with(url)


@patch("kaizen.helpers.output.nest_asyncio.apply")
@pytest.mark.asyncio
async def test_get_web_html_only_comments(mock_apply, mock_get_html):
    url = "https://cloudcode.ai"
    html_content = "<html><body><!-- Comment --></body></html>"
    mock_get_html.return_value = html_content

    result = await get_web_html(url)

    assert "<!-- Comment -->" not in result
    assert mock_apply.called
    mock_get_html.assert_called_once_with(url)


@patch("kaizen.helpers.output.nest_asyncio.apply")
@pytest.mark.asyncio
async def test_get_web_html_error_handling(mock_apply, mock_get_html):
    url = "https://cloudcode.ai"
    mock_get_html.side_effect = Exception("Network error")

    with pytest.raises(Exception, match="Network error"):
        await get_web_html(url)

    assert mock_apply.called
    mock_get_html.assert_called_once_with(url)
