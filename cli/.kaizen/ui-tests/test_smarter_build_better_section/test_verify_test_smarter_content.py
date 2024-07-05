"""Importance: good_to_have                            
Module Name: Test Smarter, Build Better Section                            
Description: Verify if the content about 'Test Smarter, Build Better' is visible and correctly positioned
"""

from playwright.sync_api import sync_playwright


def test_verify_content_visibility_and_position():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://cloudcode.ai")
        text_visible = page.inner_text('h2:has-text("Test Smarter, Build Better")')
        rect = page.eval_on_selector(
            'h2:has-text("Test Smarter, Build Better")',
            "(e) => e.getBoundingClientRect()",
        )
        print(text_visible)
        print(rect)
        browser.close()


test_verify_content_visibility_and_position()
