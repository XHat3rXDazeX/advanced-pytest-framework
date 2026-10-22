import pytest
import sys
import os
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

def test_login_page_visual_snapshot(page, env_config, browser_name):
    """
    Captures a full-page visual layout snapshot of the authentication screen 
    and validates it pixel-by-pixel against an environment-isolated baseline file.
    """
    # 1. Skip on the cloud runner to bypass OS font rendering differences entirely
    if os.environ.get("CI") == "true":
        pytest.skip("Skipping visual layout snapshot checks in headless CI cloud environments.")

    # 2. Navigate to the landing page
    page.goto(env_config["base_url"])
    page.wait_for_selector(".login_wrapper", state="visible")
    
    # 3. Establish your baseline paths cleanly using standard paths
    os_platform = sys.platform
    snapshot_dir = os.path.join("tests", "snapshots", os_platform)
    os.makedirs(snapshot_dir, exist_ok=True)
    
    baseline_path = os.path.join(snapshot_dir, f"login_page_{browser_name}_baseline.png")
    current_screenshot = page.screenshot(full_page=True)
    
    # 4. If the baseline image doesn't exist locally yet, create it on the first run!
    if not os.path.exists(baseline_path):
        with open(baseline_path, "wb") as f:
            f.write(current_screenshot)
        pytest.skip(f"Master baseline generated at {baseline_path}. Re-run test to validate.")
        
    # 5. Read the master baseline image file and compare bytes directly
    with open(baseline_path, "rb") as f:
        baseline_bytes = f.read()
        
    assert current_screenshot == baseline_bytes, f"Visual regression mismatch detected against {baseline_path}!"
