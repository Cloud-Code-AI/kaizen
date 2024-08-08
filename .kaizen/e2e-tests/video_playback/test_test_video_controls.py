'''Importance: good_to_have                            
Module Name: Video Playback                            
Description: Check if video controls are functional.
'''

import time
from playwright.sync_api import sync_playwright

class VideoPage:
    def __init__(self, page):
        self.page = page
        self.video_selector = "video"

    def play_video(self):
        self.page.click(f"{self.video_selector} [title='Play']")
        time.sleep(2)  # Wait for the video to play

    def pause_video(self):
        self.page.click(f"{self.video_selector} [title='Pause']")
        time.sleep(2)  # Wait for the video to pause

    def adjust_volume(self, volume_level):
        self.page.evaluate(f"document.querySelector('{self.video_selector}').volume = {volume_level}")

    def is_video_playing(self):
        return self.page.evaluate(f"document.querySelector('{self.video_selector}').paused") == False

    def is_video_paused(self):
        return self.page.evaluate(f"document.querySelector('{self.video_selector}').paused") == True

def test_video_controls():
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://cloudcode.ai")

        video_page = VideoPage(page)

        # Test Play
        video_page.play_video()
        assert video_page.is_video_playing(), "Video should be playing."

        # Test Pause
        video_page.pause_video()
        assert video_page.is_video_paused(), "Video should be paused."

        # Test Volume Adjustment
        video_page.adjust_volume(0.5)  # Set volume to 50%
        time.sleep(1)  # Wait for volume to adjust

        # Play again to check functionality
        video_page.play_video()
        assert video_page.is_video_playing(), "Video should be playing again."

        # Close the browser
        browser.close()

if __name__ == "__main__":
    test_video_controls()