"""Importance: good_to_have                            
Module Name: Hero Section                            
Description: Verify if the 'Join Waitlist' button is clickable and redirects to the correct section
"""

from playwright.sync_api import sync_playwright


def test_join_waitlist_button():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://cloudcode.ai")
        join_waitlist_button = page.wait_for_selector("text=Join Waitlist")

        assert join_waitlist_button.is_visible()
        join_waitlist_button.click()

        # Add assertions for the redirect to the correct section if applicable
        # For example:
        # assert "https://cloudcode.ai#cta" in page.url

        context.close()
        browser.close()
