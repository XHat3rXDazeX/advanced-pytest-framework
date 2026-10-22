import json
import os
import pytest
from playwright.sync_api import Page

# 1. Helper function to load and parse the JSON dataset
def load_test_data():
    file_path = os.path.join(os.path.dirname(__file__), "test_data.json")
    with open(file_path, "r") as file:
        return json.load(file)

# 2. Injecting the JSON objects straight into the Pytest parametrizing loop
@pytest.mark.parametrize("data", load_test_data())
def test_user_login_scenarios(page: Page, data: dict):
    """
    Drives multiple login authentication verifications dynamically 
    using a completely decoupled external JSON configuration matrix.
    """
    print(f"\nExecuting Data-Driven Scenario: {data['scenario']}")
    
    # Navigate to a standard mock login testing interface
    page.goto("https://saucedemo.com")
    
    # Fill out the authentication parameters using the data matrix fields
    page.fill("input[data-test='username']", data["username"])
    page.fill("input[data-test='password']", "secret_sauce")
    
    # Execute submission action
    page.click("input[data-test='login-button']")
    
    # Assert that the application state matches our expected URL outcome parameter
    assert data["expected_url_keyword"] in page.url
