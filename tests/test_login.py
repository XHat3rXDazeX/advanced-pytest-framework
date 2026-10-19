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
