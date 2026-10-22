import pytest
import sys
from playwright.sync_api import Page
from pages.login_page import LoginPage
# We import our configuration class
from config.settings import Settings

@pytest.mark.smoke
def test_valid_user_can_login(page: Page):
    """Test case to verify a standard user can log in securely using config variables."""
    login_page = LoginPage(page)
    
    # 1. Navigate to the base URL configured in settings
    login_page.navigate()
    
    # 2. Call the login method using our secure central variables
    login_page.login_with_credentials(Settings.USERNAME, Settings.PASSWORD)
    
    # 3. ASSERTION: Verify the login worked
    assert "inventory.html" in page.url

def test_login_page_visual_snapshot(page, env_config, browser_name, snapshot):
    """
    Captures a full-page visual layout snapshot of the authentication screen 
    and validates it pixel-by-pixel against an environment-isolated baseline file.
    """
    # 1. Navigate to the application landing page using your environment config
    page.goto(env_config["base_url"])
    
    # 2. Wait for the main page container to finish rendering completely
    page.wait_for_selector(".login_wrapper", state="visible")
    
    # 3. Take a binary screenshot image of the current page layout
    current_screenshot = page.screenshot(full_page=True)
    
    # 4. Dynamically detect operating system platform (e.g., win32, linux)
    os_platform = sys.platform
    
    # 5. Isolate our storage paths by OS platform
    snapshot.snapshot_dir = f"tests/snapshots/{os_platform}"
    
    # 6. Append browser_name so chromium, firefox, and webkit get unique files!
    snapshot.assert_match(current_screenshot, f"login_page_{browser_name}_baseline.png")
