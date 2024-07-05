"""Importance: good_to_have                            
Module Name: AI QA Assistant Section                            
Description: Verify if the content about 'AI QA Assistant' is visible and correctly positioned
"""

# Import the required libraries
from playwright.sync_api import sync_playwright


# Define the test function
def test_verify_ai_content():
    with sync_playwright() as p:
        # Open the browser and create a context
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the URL
        page.goto("https://cloudcode.ai")

        # Verify if the content about 'AI QA Assistant' is visible and correctly positioned
        ai_content = page.locator("text=AI QA Assistant")
        assert ai_content.is_visible()
        assert (
            ai_content.bounding_box["y"] > 0
        )  # Assuming y > 0 indicates correct position

        # Close the browser
        context.close()
