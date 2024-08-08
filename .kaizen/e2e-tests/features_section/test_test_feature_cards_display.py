'''Importance: good_to_have                            
Module Name: Features Section                            
Description: Check if all feature cards are displayed.
'''

# Import necessary modules
from playwright.sync_api import sync_playwright

# Define the Page Object Model for the Features section
class FeaturesPage:
    def __init__(self, page):
        self.page = page
        # Update with the correct selector for feature cards
        self.feature_cards_selector = '.flex.flex-col.gap-y-4.items-center.border.p-6.rounded-2xl.shadow-lg'  

    def get_feature_cards(self):
        """Return all feature cards found on the page."""
        return self.page.query_selector_all(self.feature_cards_selector)

# Define the test function
def test_feature_cards_displayed():
    with sync_playwright() as p:
        # Launch the browser in headless mode for CI/CD
        browser = p.chromium.launch(headless=True)  # Set headless=True for CI/CD
        page = browser.new_page()
        
        # Step 1: Navigate to the URL
        page.goto('https://cloudcode.ai')

        # Step 2: Create an instance of the FeaturesPage
        features_page = FeaturesPage(page)

        # Step 3: Wait for the feature cards section to load
        page.wait_for_selector(features_page.feature_cards_selector)

        # Step 4: Get the feature cards
        feature_cards = features_page.get_feature_cards()

        # Step 5: Verify the number of feature cards
        expected_count = 8  # Update with the expected number of feature cards
        assert len(feature_cards) == expected_count, f"Expected {expected_count} feature cards, but found {len(feature_cards)}."

        # Optional: Capture a screenshot for verification
        page.screenshot(path='feature_cards_displayed.png')

        # Close the browser
        browser.close()

# Run the test
if __name__ == "__main__":
    test_feature_cards_displayed()