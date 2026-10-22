import pytest
import logging
from playwright.sync_api import Page, expect

# Hook into our enterprise logger
logger = logging.getLogger("AutomationSuite")

def test_mobile_responsive_login_layout(playwright):
    """
    Automating UI structural validation inside an emulated Pixel 7 mobile layout matrix.
    Verifies responsive element visibility and interaction boundaries.
    """
    logger.info("Accessing Playwright device engine to extract Pixel 7 design configurations...")
    
    # 1. Fetch exact real-world mobile device parameters
    pixel_7 = playwright.devices["Pixel 7"]
    
    # 2. Launch a completely emulated browser context matrix
    browser = playwright.chromium.launch()
    context = browser.new_context(**pixel_7)
    page = context.new_page()
    
    logger.info("Navigating to target application interface inside emulated mobile viewport...")
    page.goto("https://saucedemo.com")
    
    # 3. Meticulously verify that critical login elements scale cleanly and are visible on a mobile screen
    logger.info("Executing visibility assertions on core viewport elements...")
    expect(page.locator("input[data-test='username']")).to_be_visible()
    expect(page.locator("input[data-test='password']")).to_be_visible()
    
    # 4. Perform interaction validation loops
    page.fill("input[data-test='username']", "standard_user")
    page.fill("input[data-test='password']", "secret_sauce")
    page.click("input[data-test='login-button']")
    
    # 5. Assert that routing works correctly inside the mobile device viewport matrix
    logger.info(f"Mobile authentication successful. Current emulated path: {page.url}")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    
    # Clean up memory threads safely
    context.close()
    browser.close()
