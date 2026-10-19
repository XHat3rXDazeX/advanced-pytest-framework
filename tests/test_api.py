import pytest
from playwright.sync_api import Page

@pytest.mark.api
def test_mocked_user_details(page: Page):
    """Test case to verify framework can mock backend API data via page routing."""
    
    # 1. Intercept the URL directly inside the browser session
    page.route("https://my-local-testing-api.com", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"name": "Leanne Graham", "email": "Sincere@april.biz"}'
    ))
    
    # 2. Trigger the page to hit our local mock route
    page.goto("https://my-local-testing-api.com")
    
    # 3. Read the text displayed right on the screen
    response_text = page.locator("body").inner_text()
    
    # 4. ASSERTION: Verify our local mock text matches perfectly
    assert "Leanne Graham" in response_text
    assert "Sincere@april.biz" in response_text
