'''Importance: critical                            
Module Name: Accessibility Features                            
Description: Check for ARIA labels on interactive elements.
'''


### Step 2: Create the Page Object Model
Create a file named `page.py` to encapsulate the page interactions and elements.

```python
# page.py
from playwright.sync_api import Page

class HomePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url)

    def get_interactive_elements(self):
        return self.page.query_selector_all('button, a, [role="button"], [role="link"]')

    def get_aria_label(self, element):
        return element.get_attribute('aria-label')
```

### Step 3: Write the Test Script
Create a file named `test_aria_labels.py` for the test script.

```python
# test_aria_labels.py
import pytest
from playwright.sync_api import sync_playwright
from page import HomePage

@pytest.mark.parametrize("url", ["https://cloudcode.ai", "https://another-url.com"])
def test_aria_labels(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode
        page = browser.new_page()
        home_page = HomePage(page)

        # Navigate to the URL
        home_page.navigate(url)

        # Get interactive elements
        elements = home_page.get_interactive_elements()

        # Check for ARIA labels
        for element in elements:
            aria_label = home_page.get_aria_label(element)
            assert aria_label is not None, f"Element {element} is missing aria-label"
            assert aria_label.strip() != "", f"Element {element} has an empty aria-label"

        browser.close()
```

### Step 4: Capture Screenshots on Failure (Optional)
You can enhance the test to capture screenshots in case of failures. Modify the test function as follows:

```python
# test_aria_labels.py
import pytest
from playwright.sync_api import sync_playwright
from page import HomePage

@pytest.mark.parametrize("url", ["https://cloudcode.ai", "https://another-url.com"])
def test_aria_labels(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        home_page = HomePage(page)

        try:
            # Navigate to the URL
            home_page.navigate(url)

            # Get interactive elements
            elements = home_page.get_interactive_elements()

            # Check for ARIA labels
            for element in elements:
                aria_label = home_page.get_aria_label(element)
                assert aria_label is not None, f"Element {element} is missing aria-label"
                assert aria_label.strip() != "", f"Element {element} has an empty aria-label"

        except AssertionError as e:
            page.screenshot(path='screenshot.png')
            raise e
        finally:
            browser.close()
```

### Step 5: Run Tests in Parallel
To run tests in parallel, ensure you have `pytest-xdist` installed:
```bash
pip install pytest-xdist
```
Then, you can run your tests with:
```bash
pytest -n auto