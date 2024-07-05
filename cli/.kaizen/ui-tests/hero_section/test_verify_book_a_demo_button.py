"""Importance: good_to_have                            
Module Name: Hero Section                            
Description: Verify if the 'Book a Demo' button is clickable and redirects to the correct section
"""

import pytest
from playwright.sync_api import sync_playwright


class TestCloudCodeAI:
    @pytest.fixture(scope="function")
    def browser(self):
        # Open a browser page in incognito mode
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(storage_state=None, accept_downloads=True)
            page = context.new_page()
            yield page
            browser.close()

    def test_book_demo_button_redirects_to_section(self, browser):
        # Navigate to the Cloud Code AI website
        browser.goto("https://cloudcode.ai")

        # Get the 'Book a Demo' button element
        book_demo_button = browser.wait_for_selector("text=Book a Demo")

        # Assert that the 'Book a Demo' button is visible and enabled
        assert book_demo_button.is_visible()
        assert book_demo_button.is_enabled()

        # Click the 'Book a Demo' button
        book_demo_button.click()

        # Wait for the navigation to complete
        browser.wait_for_navigation()

        # Assert that the URL has changed to the expected section
        assert "cta" in browser.url

        # Take a screenshot for visual verification
        browser.screenshot(path="book_demo_button_click.png")
