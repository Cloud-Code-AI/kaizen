"""Importance: good_to_have                            
Module Name: Partner Logos Section                            
Description: Verify if all partner logos are visible and displayed correctly
"""

from playwright.sync_api import sync_playwright


def test_partner_logos_visibility():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://cloudcode.ai")
        partner_logos = page.query_selector_all(
            ".flex.w-full.gap-x-4.items-center.justify-center > img"
        )

        for logo in partner_logos:
            assert logo.is_visible()
            assert logo.bounding_box["width"] > 0
            assert logo.bounding_box["height"] > 0

        context.close()
        browser.close()
