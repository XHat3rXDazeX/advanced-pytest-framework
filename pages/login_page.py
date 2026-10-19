from playwright.sync_api import Page
# We import our central configuration settings
from config.settings import Settings

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("input[id='user-name']")
        self.password_input = page.locator("input[id='password']")
        self.login_button = page.locator("input[id='login-button']")

    def navigate(self):
        """Action method to visit the site using our central config URL."""
        self.page.goto(Settings.BASE_URL) 

    def login_with_credentials(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
