import pytest
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

def test_login_page_visual_snapshot(page, env_config, snapshot):
    """
    Captures a full-page visual layout snapshot of the authentication screen 
    and validates it pixel-by-pixel against a golden baseline snapshot file.
    """
    # 1. Navigate to the application landing page using your environment config
    page.goto(env_config["base_url"])
    
    # 2. Wait for the main page container to finish rendering completely
    page.wait_for_selector(".login_wrapper", state="visible")
    
    # 3. Take a binary screenshot image of the current page layout
    current_screenshot = page.screenshot(full_page=True)
    
    # 4. Assert that the captured screenshot exactly matches the saved baseline file
    # This creates a folder named 'snapshots' inside your tests directory
    snapshot.assert_match(current_screenshot, "login_page_baseline.png")
