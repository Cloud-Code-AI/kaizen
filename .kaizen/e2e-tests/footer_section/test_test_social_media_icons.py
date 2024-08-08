'''Importance: good_to_have                            
Module Name: Footer Section                            
Description: Verify the presence of social media icons.
'''

/my_playwright_tests
├── tests
│   └── test_social_media_icons.py
├── pages
│   └── social_media_page.py
└── requirements.txt
```

### Step 1: Install Playwright
Make sure to install Playwright if you haven't already:
```bash
pip install playwright
playwright install
```

### Step 2: Create the Page Object Model
Create the file `pages/social_media_page.py` with the following content:

```python
# pages/social_media_page.py
from playwright.sync_api import Page

class SocialMediaPage:
    def __init__(self, page: Page):
        self.page = page
        self.github_icon = "img[src*='github']"
        self.linkedin_icon = "img[src*='linkedin']"
        self.twitter_icon = "img[src*='twitter']"

    def navigate(self, url: str):
        self.page.goto(url)

    def is_icon_visible(self, icon_selector: str) -> bool:
        return self.page.is_visible(icon_selector)
```

### Step 3: Write the Test Script
Create the file `tests/test_social_media_icons.py` with the following content:

```python
# tests/test_social_media_icons.py
import os
import pytest
from playwright.sync_api import sync_playwright
from pages.social_media_page import SocialMediaPage

@pytest.mark.parametrize("icon_selector", [
    "img[src*='github']",
    "img[src*='linkedin']",
    "img[src*='twitter']"
])
def test_social_media_icons(icon_selector):
    with sync_playwright() as p:
        # Launch the browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        social_media_page = SocialMediaPage(page)

        # Navigate to the page
        social_media_page.navigate("https://cloudcode.ai")

        # Check if the icon is visible
        if not social_media_page.is_icon_visible(icon_selector):
            # Create a directory for screenshots if it doesn't exist
            os.makedirs("screenshots", exist_ok=True)
            # Capture a screenshot
            page.screenshot(path=f"screenshots/{icon_selector.split('=')[1].strip('\'\"')}.png")
        
        assert social_media_page.is_icon_visible(icon_selector), f"{icon_selector} is not visible"

        # Close the browser
        browser.close()
```

### Step 4: Run the Tests
You can run your tests using pytest:
```bash
pytest tests/test_social_media_icons.py
```

### Step 5: Capture Screenshots
The test script already includes logic to capture screenshots if an icon is not visible. The screenshots will be saved in a `screenshots` directory.

### Step 6: Integrate with CI/CD
Make sure to include the necessary commands in your CI/CD configuration file to run the tests. For example, in a GitHub Actions workflow, you might have:

```yaml
name: Run Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install playwright
          playwright install
          pip install pytest

      - name: Run tests
        run: pytest tests/test_social_media_icons.py