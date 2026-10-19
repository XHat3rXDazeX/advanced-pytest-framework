import os

class Settings:
    # Target application URLs
    BASE_URL = "https://saucedemo.com"
    API_URL = "https://my-local-testing-api.com"
    
    # Test Accounts (We use default safe strings, but allow environment overrides)
    USERNAME = os.getenv("TEST_USER", "standard_user")
    PASSWORD = os.getenv("TEST_PASSWORD", "secret_sauce")
