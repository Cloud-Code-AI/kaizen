'''Importance: good_to_have                            
Module Name: Responsive Design                            
Description: Verify layout on tablet devices.
'''

import pytest
from playwright.sync_api import sync_playwright

class CloudCodePage:
    def __init__(self, page):
        self.page = page
        self.header_selector = 'header'
        self.hero_section_selector = '#hero'
        self.signup_button_selector = 'a[href="https://beta.cloudcode.ai"]'
        self.video_selector = 'video'

    def navigate(self, url):
        self.page.goto(url)

    def verify_header(self):
        assert self.page.is_visible(self.header_selector), "Header is not visible"

    def verify_hero_section(self):
        assert self.page.is_visible(self.hero_section_selector), "Hero section is not visible"

    def verify_signup_button(self):
        assert self.page.is_visible(self.signup_button_selector), "Signup button is not visible"

    def verify_video(self):
        assert self.page.is_visible(self.video_selector), "Video is not visible"

    def capture_screenshot(self, filename):
        self.page.screenshot(path=filename)

@pytest.mark.parametrize("viewport", [{"width": 768, "height": 1024}])
def test_layout_on_tablet(viewport):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode
        context = browser.new_context(viewport=viewport)
        page = context.new_page()
        
        cloud_code_page = CloudCodePage(page)
        cloud_code_page.navigate("https://cloudcode.ai")
        
        cloud_code_page.verify_header()
        cloud_code_page.verify_hero_section()
        cloud_code_page.verify_signup_button()
        cloud_code_page.verify_video()
        
        cloud_code_page.capture_screenshot("tablet_layout_verification.png")
        
        context.close()
        browser.close()

if __name__ == "__main__":
    pytest.main()