"""Importance: good_to_have                            
Module Name: Join Waitlist Section                            
Description: Verify if the 'Join Waitlist' form is functional and accepts valid email addresses
"""

from playwright.sync_api import sync_playwright


def test_join_waitlist():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://cloudcode.ai")
        page.click("text=Join Waitlist")
        page.fill("input[name='email']", "test@example.com")
        page.click("button:has-text('Submit')")

        # Add assertions or further actions as needed

        page.screenshot(path="join_waitlist.png")

        browser.close()
