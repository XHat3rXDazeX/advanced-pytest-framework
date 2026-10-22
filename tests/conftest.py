import os
import logging
import pytest
from datetime import datetime

# 1. Initialize a production-grade centralized logging subsystem
@pytest.fixture(scope="session", autouse=True)
def configure_logger():
    """
    Initializes a central logging subsystem that captures execution metrics 
    and pipes them simultaneously to the console and a historical automation.log file.
    """
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger("AutomationSuite")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # File Handler - Writes deep historical logs to local disk
        log_file = os.path.join(log_dir, "automation.log")
        file_handler = logging.FileHandler(log_file, mode="w")
        file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
    return logger

# 2. Hooks into Pytest execution to automatically capture failure screenshots
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hooks into Pytest execution to automatically capture a browser screenshot 
    on test failure and seamlessly embed it into the generated HTML report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "page" in item.fixturenames:
            page = item.funcargs["page"]
            
            screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"fail_{item.name}_{timestamp}.png")
            
            page.screenshot(path=screenshot_path)
            
            import pytest_html
            if hasattr(report, "extra"):
                relative_path = os.path.join("screenshots", f"fail_{item.name}_{timestamp}.png")
                html_element = pytest_html.extras.image(relative_path)
                report.extra.append(html_element)