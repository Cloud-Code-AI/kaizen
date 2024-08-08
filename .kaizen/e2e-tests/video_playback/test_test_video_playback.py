'''Importance: good_to_have                            
Module Name: Video Playback                            
Description: Verify that the demo video plays without issues.
'''


### Step 2: Create the Page Object Model (POM)

Create a file named `video_page.py`:

```python
# video_page.py
from playwright.sync_api import Page

class VideoPage:
    def __init__(self, page: Page):
        self.page = page
        self.video_selector = "video"

    def navigate(self, url: str):
        self.page.goto(url)

    def play_video(self):
        video = self.page.locator(self.video_selector)
        video.click()  # Click to play the video

    def is_video_playing(self):
        # Check if the video is playing
        return self.page.evaluate("!document.querySelector('video').paused")

    def take_screenshot(self, filename: str):
        self.page.screenshot(path=filename)
```

### Step 3: Write the Test Script

Create a file named `test_video_playback.py`:

```python
# test_video_playback.py
import pytest
from playwright.sync_api import sync_playwright
from video_page import VideoPage

@pytest.mark.parametrize("url", ["https://cloudcode.ai"])
def test_video_playback(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode
        page = browser.new_page()
        video_page = VideoPage(page)

        video_page.navigate(url)
        video_page.play_video()

        # Wait for a few seconds to allow the video to play
        page.wait_for_timeout(5000)

        assert video_page.is_video_playing(), "The video is not playing."

        # Take a screenshot for verification
        video_page.take_screenshot("video_playback.png")

        browser.close()
```

### Step 4: Run the Tests

You can execute the test using pytest:

```bash
pytest test_video_playback.py