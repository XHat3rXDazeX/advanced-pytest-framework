import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from config.settings import Settings

@pytest.mark.regression
def test_user_can_complete_checkout_flow(page: Page):
    """Verifies an E2E e-commerce transaction completes and asserts receipt headers."""
    login_page = LoginPage(page)
    
    # 1. Step into the application session
    login_page.navigate()
    login_page.login_with_credentials(Settings.USERNAME, Settings.PASSWORD)
    
    # 2. Execute the full structural purchase logic
    login_page.purchase_backpack_flow("Harsukh", "QA", "L6P 0A1")
    
    # 3. CRITICAL ASSERTION: Verify the success confirmation banner is visible
    # This proves the database transaction and front-end state are perfectly aligned!
    assert login_page.complete_header.inner_text() == "Thank you for your order!"
