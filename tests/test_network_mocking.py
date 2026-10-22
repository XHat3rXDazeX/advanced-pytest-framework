import pytest
from playwright.sync_api import Page, expect

def test_asset_failure_resilience(page: Page):
    """
    Simulates a static content delivery network (CDN) drop by intercepting 
    all outbound image assets (.png) and forcing a mock 404 Not Found status.
    """
    # 1. Intercept all outbound requests for PNG images and block them
    page.route(
        "**/*.png", 
        lambda route: route.fulfill(
            status=404,
            content_type="image/png"
        )
    )
    
    # 2. Navigate to the test interface
    page.goto("https://saucedemo.com")
    
    # 3. Perform a standard login sequence
    page.fill("input[data-test='username']", "standard_user")
    page.fill("input[data-test='password']", "secret_sauce")
    page.click("input[data-test='login-button']")
    
    print(f"\nSuccessfully blocked image assets. Verifying page stability: {page.url}")
    
    # 4. Assert that the core application framework handled the broken asset server safely
    # (The page should still load its layout and text content completely fine)
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
