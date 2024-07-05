"""Importance: critical                            
Module Name: Page Title and Meta Description                            
Description: Verify if the meta description is present and contains relevant information about the application
"""

from playwright.sync_api import sync_playwright


def test_meta_description_presence_and_content():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the URL
        page.goto("https://cloudcode.ai")

        # Get the meta description content
        meta_description = page.evaluate(
            """() => {
            const metaTag = document.querySelector('meta[name="description"]');
            return metaTag ? metaTag.content : null;
        }"""
        )

        # Validate the presence and content of the meta description
        assert meta_description is not None, "Meta description is missing on the page"
        assert (
            "CloudCode AI" in meta_description
        ), "Meta description does not contain relevant information"

        # Close the browser
        browser.close()


test_meta_description_presence_and_content()
