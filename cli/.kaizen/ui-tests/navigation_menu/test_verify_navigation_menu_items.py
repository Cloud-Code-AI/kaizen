"""Importance: critical                            
Module Name: Navigation Menu                            
Description: Click on each navigation menu item and verify if the respective section is scrolled into view or loaded
"""

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def browser():
    # Open the browser
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()


def test_navigation_menu(browser):
    page = browser.new_page()
    page.goto("https://cloudcode.ai")

    # Click on each navigation menu item and verify if the respective section is scrolled into view or loaded
    navigation_items = page.query_selector_all("header nav a")
    for item in navigation_items:
        item.click()
        section_id = item.get_attribute("href")
        section = page.query_selector(section_id)
        assert section.is_visible()

    # Close the page
    page.close()
