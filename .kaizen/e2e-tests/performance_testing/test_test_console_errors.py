'''Importance: good_to_have                            
Module Name: Performance Testing                            
Description: Check for any console errors.
'''

/tests
  ├── __init__.py
  ├── test_console_errors.py
  └── page_objects
      ├── __init__.py
      └── base_page.py
```

### Step 1: Install Playwright
Ensure you have Python 3.9 installed, and then install Playwright and its dependencies:

```bash
pip install playwright
playwright install
```

### Step 2: Implement the Base Page Class
Create the `base_page.py` file in the `page_objects` directory:

```python
# page_objects/base_page.py
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        self.page.goto(url)
```

### Step 3: Write the Test Script
Create the `test_console_errors.py` file in the `tests` directory:

```python
# tests/test_console_errors.py
import pytest
from playwright.sync_api import sync_playwright
from page_objects.base_page import BasePage

@pytest.fixture(scope="module")
def setup_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set headless=True for headless mode
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

def test_console_errors(setup_browser):
    context = setup_browser
    page = context.new_page()
    base_page = BasePage(page)

    # Capture console messages
    console_errors = []

    def handle_console_message(msg):
        if msg.type == 'error':
            console_errors.append(msg.text)

    page.on("console", handle_console_message)

    # Navigate to the URL
    base_page.navigate_to("https://cloudcode.ai")

    # Wait for a few seconds to allow all console messages to be logged
    page.wait_for_timeout(5000)

    # Assert that there are no console errors
    assert len(console_errors) == 0, f"Console errors found: {console_errors}"

    # Optionally, take a screenshot for debugging
    page.screenshot(path="screenshot.png")

    # Close the page
    page.close()
```

### Step 4: Run the Test
Use pytest to execute the test:

```bash
pytest tests/test_console_errors.py