"""Importance: critical                            
Module Name: Page Title and Meta Description                            
Description: Verify if the title is 'Cloud Code AI - An AI Co-Pilot for your Cloud resources!'
"""

import pytest
from playwright.sync_api import sync_playwright


def test_verify_title():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://cloudcode.ai")
        title = page.title()
        assert title == "Cloud Code AI - An AI Co-Pilot for your Cloud resources!"
        browser.close()


# Run the test
pytest.main([__file__])
