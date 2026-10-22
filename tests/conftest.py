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

# 3. Register a custom command-line flag option for the framework
def pytest_addoption(parser):
    parser.addoption(
        "--env", 
        action="store", 
        default="qa", 
        help="Target environment environment matrix matrix selection: qa or prod"
    )

# 4. Inject the parsed CLI option into a reusable fixture setup
@pytest.fixture(scope="session")
def env_config(request):
    """
    Dynamically maps configuration metadata contexts based on 
    the runtime --env flag passed into the terminal configuration loop.
    """
    target_env = request.config.getoption("--env")
    
    # Update both environments to include the missing www. prefix string
    config_matrix = {
        "qa": "https://www.saucedemo.com",
        "prod": "https://www.saucedemo.com"
    }
    
    selected_url = config_matrix.get(target_env, config_matrix["qa"])
    return {"base_url": selected_url, "environment": target_env}
