from playwright.sync_api import Page
from config.settings import Settings

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        # Login Selectors
        self.username_input = page.locator("input[id='user-name']")
        self.password_input = page.locator("input[id='password']")
        self.login_button = page.locator("input[id='login-button']")
        
        # Advanced Checkout Selectors
        self.add_backpack_button = page.locator("button[id='add-to-cart-sauce-labs-backpack']")
        self.shopping_cart_link = page.locator("a[class='shopping_cart_link']")
        self.checkout_button = page.locator("button[id='checkout']")
        
        # Checkout Form Information
        self.first_name_input = page.locator("input[id='first-name']")
        self.last_name_input = page.locator("input[id='last-name']")
        self.postal_code_input = page.locator("input[id='postal-code']")
        self.continue_button = page.locator("input[id='continue']")
        self.finish_button = page.locator("button[id='finish']")
        self.complete_header = page.locator("h2[class='complete-header']")

    def navigate(self):
        self.page.goto(Settings.BASE_URL) 

    def login_with_credentials(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def purchase_backpack_flow(self, first_name: str, last_name: str, postal_code: str):
        """Executes a full multi-step checkout workflow sequentially."""
        self.add_backpack_button.click()
        self.shopping_cart_link.click()
        self.checkout_button.click()
        
        # Fill Checkout Information Form
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()
        
        # Complete Purchase - Wait for visibility to handle WebKit layout engine rendering speeds
        self.finish_button.wait_for(state="visible")
        self.finish_button.click()
