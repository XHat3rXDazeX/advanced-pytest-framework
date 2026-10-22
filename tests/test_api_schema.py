import json
import os
import logging
import pytest
from playwright.sync_api import APIRequestContext

# Connect into our centralized logging architecture channel
logger = logging.getLogger("AutomationSuite")

def load_expected_schema():
    file_path = os.path.join(os.path.dirname(__file__), "schema_match.json")
    with open(file_path, "r") as file:
        return json.load(file)

def test_backend_api_endpoint_validation(playwright):
    """
    Directly targets back-end application layers to assert API response codes,
    header integrity, and structural payload data compliance.
    """
    logger.info("Initializing background API Request Context...")
    
    # 1. Establish an isolated background HTTP requester
    api_context = playwright.request.new_context(base_url="https://httpbin.org")
    
    logger.info("Sending outbound POST request to validation endpoint...")
    expected_data = load_expected_schema()
    
    # 2. Dispatch a payload to a real, open test server endpoint
    response = api_context.post("/post", data=expected_data)
    
    # 3. Assert the HTTP response status code is a perfect 200 OK
    logger.info(f"API Response intercepted. Status Code: {response.status}")
    assert response.status == 200
    
    # 4. Parse the return JSON data packet
    response_body = response.json()
    returned_payload = response_body["json"]
    
    # 5. Execute core data structure validation assertions
    logger.info("Verifying payload data schema values and key types...")
    assert returned_payload["account_status"] == "active"
    assert isinstance(returned_payload["user_id"], int)
    assert "auth_token" in returned_payload
    
    logger.info("API Schema compliance check successfully passed.")
    api_context.dispose()
