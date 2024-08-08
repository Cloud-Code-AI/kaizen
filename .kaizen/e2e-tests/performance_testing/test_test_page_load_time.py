'''Importance: good_to_have                            
Module Name: Performance Testing                            
Description: Measure page load time.
'''

playwright_tests/
│
├── tests/
│   ├── page.py
│   └── test_page_load_time.py
```

### Step 1: Install Dependencies
Make sure you have Python 3.9 and Playwright installed:
```bash
pip install playwright
playwright install
```

### Step 2: Implement the Page Object Model (POM)
Create the `page.py` file in the `tests` directory:

```python
# tests/page.py
from playwright.sync_api import Page

class CloudCodePage:
    def __init__(self, page: Page):
        self.page = page

    async def navigate(self, url: str):
        await self.page.goto(url)
```

### Step 3: Write the Test Script
Create the `test_page_load_time.py` file in the `tests` directory:

```python
# tests/test_page_load_time.py
import time
import pytest
from playwright.sync_api import sync_playwright
from page import CloudCodePage

@pytest.mark.asyncio
async def test_page_load_time():
    url = "https://cloudcode.ai"
    
    async with sync_playwright() as p:
        # Launch the browser in headless mode
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        cloud_code_page = CloudCodePage(page)

        # Measure page load time
        start_time = time.time()
        await cloud_code_page.navigate(url)
        load_time = time.time() - start_time

        print(f"Page load time: {load_time:.2f} seconds")

        await browser.close()
```

### Step 4: Optional - Capture Additional Metrics
If you want to capture performance metrics, you can extend the test as follows:

```python
async def test_page_load_time_with_metrics():
    url = "https://cloudcode.ai"
    
    async with sync_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Start measuring performance
        await page.goto(url)
        performance = await page.evaluate("JSON.stringify(window.performance.toJSON())")
        print(performance)

        await browser.close()
```

### Step 5: Run the Test
You can run your test using pytest:

```bash
pytest tests/test_page_load_time.py