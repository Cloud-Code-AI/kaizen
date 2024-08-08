'''Importance: critical                            
Module Name: Hero Section                            
Description: Verify the presence of the demo video.
'''

your_project/
│
├── pages/
│   └── cloudcode_page.py
│
├── tests/
│   └── test_demo_video.py
│
└── README.md
```

### 1. **Page Object Model Implementation**

**File: `pages/cloudcode_page.py`**

```python
from playwright.sync_api import Page

class CloudCodePage:
    def __init__(self, page: Page):
        self.page = page
        self.video_selector = "video[src='/demo.mp4']"

    def navigate(self):
        self.page.goto("https://cloudcode.ai")

    def is_video_present(self) -> bool:
        return self.page.is_visible(self.video_selector)
```

### 2. **Test Script Implementation**

**File: `tests/test_demo_video.py`**

```python
import pytest
from playwright.sync_api import sync_playwright
from pages.cloudcode_page import CloudCodePage

@pytest.mark.parametrize("url", ["https://cloudcode.ai"])
def test_demo_video_presence(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode
        page = browser.new_page()
        cloud_code_page = CloudCodePage(page)

        cloud_code_page.navigate()
        assert cloud_code_page.is_video_present(), "Demo video is not present on the page."

        browser.close()
```

### 3. **Running the Tests**

To run the tests, execute the following command in your terminal:

```bash
pytest tests/
```

### 4. **Integrate with CI/CD Pipeline**

Make sure to configure your CI/CD pipeline to:

- Install dependencies:
  ```bash
  pip install playwright
  playwright install
  ```

- Run the tests in headless mode as shown in the test script.

### 5. **Documentation**

Create a `README.md` file in your project root with the following content:

```markdown
# Playwright Test for CloudCode AI

## Setup Instructions

1. Ensure Python 3.9 is installed.
2. Install Playwright and necessary dependencies:
   ```bash
   pip install playwright
   playwright install
   ```

## Running Tests

To run the tests, execute:
```bash
pytest tests/
```

## CI/CD Integration

Ensure your CI/CD pipeline installs the dependencies and runs the tests in headless mode.