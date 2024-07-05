"""Importance: good_to_have                            
Module Name: Social Links Section                            
Description: Verify if all social links are visible and functional
"""

from playwright.sync_api import sync_playwright


def test_social_links_are_visible_and_functional():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://cloudcode.ai")
        page.wait_for_load_state("networkidle")

        social_links = page.query_selector_all("img[alt='social_link']")
        for link in social_links:
            assert link.is_visible()
            link.click()
            context.wait_for_page()
            assert "cloudcode.ai" in context.url

        browser.close()


test_social_links_are_visible_and_functional()
