import pytest
import logging
from playwright.sync_api import Page, expect

# Hook into our enterprise logger
logger = logging.getLogger("AutomationSuite")

def test_mobile_responsive_login_layout(playwright, env_config):
    """
    Automating UI structural validation inside an emulated Pixel 7 layout matrix.
    Uses dynamic command-line environment parameters.
    """
    logger.info(f"Targeting deployment platform environment: {env_config['environment'].upper()}")
    
    pixel_7 = playwright.devices["Pixel 7"]
    browser = playwright.chromium.launch()
    context = browser.new_context(**pixel_7)
    page = context.new_page()
    
    # Decouple the web address by mapping it straight to our CLI fixture base URL parameter
    target_url = f"{env_config['base_url']}/"
    logger.info(f"Navigating to emulated mobile workspace endpoint: {target_url}")
    page.goto(target_url)
    
    expect(page.locator("input[data-test='username']")).to_be_visible()
    expect(page.locator("input[data-test='password']")).to_be_visible()
    
    page.fill("input[data-test='username']", "standard_user")
    page.fill("input[data-test='password']", "secret_sauce")
    page.click("input[data-test='login-button']")
    
    expect(page).to_have_url(f"{env_config['base_url']}/inventory.html")
    
    context.close()
    browser.close()