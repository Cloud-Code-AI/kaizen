import pytest
from unittest.mock import patch, AsyncMock
from bs4 import BeautifulSoup, Comment
import asyncio
import nest_asyncio

# Assuming the get_web_html function is defined in kaizen/helpers/output.py
from kaizen.helpers.output import get_web_html

@pytest.fixture
def mock_get_html():
    with patch('kaizen.helpers.output.get_html', new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_nest_asyncio():
    with patch('kaizen.helpers.output.nest_asyncio.apply') as mock:
        yield mock

@pytest.mark.parametrize("html_content, expected_output", [
    (
        """
        <html>
            <head><meta charset="UTF-8"><title>Test</title></head>
            <body>
                <svg></svg>
                <style>body {background-color: blue;}</style>
                <script>alert('Hello');</script>
                <noscript>Your browser does not support JavaScript!</noscript>
                <link rel="stylesheet" href="styles.css">
                <div><!-- This is a comment --></div>
                <p>Test paragraph</p>
            </body>
        </html>
        """,
        """
        <html>
         <body>
          <div>
          </div>
          <p>
           Test paragraph
          </p>
         </body>
        </html>
        """
    ),
    (
        "",  # Empty HTML content
        ""
    ),
    (
        "<html><body><p>Nothing to remove here!</p></body></html>",  # No removable elements
        "<html>\n <body>\n  <p>\n   Nothing to remove here!\n  </p>\n </body>\n</html>"
    ),
    (
        """
        <html>
            <head><meta charset="UTF-8"><title>Test</title></head>
            <body>
                <p>Content with head and meta tags</p>
            </body>
        </html>
        """,
        """
        <html>
         <body>
          <p>
           Content with head and meta tags
          </p>
         </body>
        </html>
        """
    )
])
async def test_get_web_html_normal_cases(mock_get_html, mock_nest_asyncio, html_content, expected_output):
    mock_get_html.return_value = html_content

    url = "https://cloudcode.ai"
    result = await get_web_html(url)

    assert result.strip() == expected_output.strip()
    mock_nest_asyncio.assert_called_once()

async def test_get_web_html_invalid_url(mock_get_html, mock_nest_asyncio):
    mock_get_html.side_effect = Exception("Network error")

    url = "https://cloudcode.ai"
    with pytest.raises(Exception, match="Network error"):
        await get_web_html(url)
    mock_nest_asyncio.assert_called_once()

async def test_get_web_html_large_content(mock_get_html, mock_nest_asyncio):
    large_html_content = "<html><body>" + "<p>Test</p>" * 10000 + "</body></html>"
    expected_output = "<html>\n <body>\n" + "  <p>\n   Test\n  </p>\n" * 10000 + " </body>\n</html>"
    mock_get_html.return_value = large_html_content

    url = "https://cloudcode.ai"
    result = await get_web_html(url)

    assert result.strip() == expected_output.strip()
    mock_nest_asyncio.assert_called_once()