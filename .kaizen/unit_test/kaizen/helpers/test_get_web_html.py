import pytest
from bs4 import BeautifulSoup, Comment
import asyncio
import nest_asyncio
from unittest.mock import patch, AsyncMock

# Assuming get_web_html is defined in kaizen/helpers/output.py
from kaizen.helpers.output import get_web_html

# Mock the get_html function
async def mock_get_html(url):
    if url == "http://valid.url":
        return """
        <html>
            <head>
                <meta charset="UTF-8">
                <link rel="stylesheet" href="styles.css">
                <style>body { background-color: #fff; }</style>
                <script src="script.js"></script>
                <noscript>Your browser does not support JavaScript!</noscript>
            </head>
            <body>
                <svg></svg>
                <h1>Title</h1>
                <p>Paragraph</p>
                <!-- This is a comment -->
            </body>
        </html>
        """
    elif url == "http://no.removable.elements":
        return """
        <html>
            <body>
                <h1>Title</h1>
                <p>Paragraph</p>
            </body>
        </html>
        """
    elif url == "http://empty.html":
        return ""
    elif url == "http://large.content":
        return "<html>" + "<p>Content</p>" * 10000 + "</html>"
    else:
        raise ValueError("Invalid URL")

@pytest.fixture
def mock_get_html_fixture():
    with patch('kaizen.helpers.output.get_html', new=mock_get_html):
        yield

@pytest.mark.parametrize("url, expected_substring", [
    ("http://valid.url", "<h1>Title</h1>"),
    ("http://no.removable.elements", "<h1>Title</h1>"),
    ("http://empty.html", ""),
    ("http://large.content", "<p>Content</p>")
])
def test_get_web_html(mock_get_html_fixture, url, expected_substring):
    result = get_web_html(url)
    assert expected_substring in result

def test_invalid_url(mock_get_html_fixture):
    with pytest.raises(ValueError, match="Invalid URL"):
        get_web_html("http://invalid.url")