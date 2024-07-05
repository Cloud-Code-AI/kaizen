"""Importance: good_to_have                            
Module Name: Smarter Code, Safer Software Section                            
Description: Verify if the content about 'Smarter Code, Safer Software' is visible and correctly positioned
"""
from playwright.sync_api import sync_playwright


def test_verify_content_visibility_and_position():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://cloudcode.ai")
        content_element = page.locator("text=Smarter Code, Safer Software")

        assert content_element.is_visible()
        assert (
            content_element.bounding_box["x"] >= 0
        )  # Adjust according to expected position
        assert (
            content_element.bounding_box["y"] >= 0
        )  # Adjust according to expected position

        browser.close()
