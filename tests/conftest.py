import os
import logging
import pytest
import json
import urllib.request
from datetime import datetime

# 1. Initialize a production-grade centralized logging subsystem (xdist-safe)
@pytest.fixture(scope="session", autouse=True)
def configure_logger():
    """
    Initializes a central logging subsystem that isolates execution metrics per parallel 
    worker to prevent multi-threaded file-locking race conditions.
    """
    log_dir = os.path.join(os.path.dirname(__file__), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Detect if pytest-xdist is running and extract the worker ID (e.g., gw0, gw1)
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    
    # Create an isolated logger name per worker
    logger = logging.getLogger(f"AutomationSuite_{worker_id}")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # Create an isolated log file per worker (e.g., automation_gw0.log)
        log_file_name = f"automation_{worker_id}.log" if worker_id != "master" else "automation.log"
        log_file = os.path.join(log_dir, log_file_name)
        
        # Use mode="a" (append) to prevent workers from aggressively locking/wiping files
        file_handler = logging.FileHandler(log_file, mode="a")
        file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
    return logger

# 2. Hooks into Pytest execution to automatically capture failure screenshots (xdist-safe)
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
            
            # Extract worker ID to make the file name completely unique across threads
            worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            screenshot_name = f"fail_{worker_id}_{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)
            
            page.screenshot(path=screenshot_path)
            
            # Safely embed into report. xdist requires checking for the extra list initialization
            import pytest_html
            if not hasattr(report, "extra"):
                report.extra = []
                
            relative_path = os.path.join("screenshots", screenshot_name)
            html_element = pytest_html.extras.image(relative_path)
            report.extra.append(html_element)

# 3. Register a custom command-line flag option for the framework
def pytest_addoption(parser):
    parser.addoption(
        "--env", 
        action="store", 
        default="qa", 
        help="Target environment matrix selection: qa or prod"
    )

# 4. Inject the parsed CLI option into a reusable fixture setup
@pytest.fixture(scope="session")
def env_config(request):
    """
    Dynamically maps configuration metadata contexts based on 
    the runtime --env flag passed into the terminal configuration loop.
    """
    target_env = request.config.getoption("--env")
    
    config_matrix = {
        "qa": "https://www.saucedemo.com",
        "prod": "https://www.saucedemo.com"
    }
    
    selected_url = config_matrix.get(target_env, config_matrix["qa"])
    return {"base_url": selected_url, "environment": target_env}


def pytest_sessionfinish(session, exitstatus):
    """
    Automated lifecycle teardown hook that aggregates execution metrics 
    and dispatches a real-time status card to a team chat webhook endpoint.
    """
    # 1. Gather core execution metrics from the internal Pytest session object
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    if reporter is None:
        return

    # Extract clean numeric metric summaries safely
    passed = len(reporter.stats.get("passed", []))
    failed = len(reporter.stats.get("failed", []))
    skipped = len(reporter.stats.get("skipped", []))
    total = passed + failed + skipped
    
    # Calculate total duration in seconds
    import time
    try:
        # Check if the internal session object exposes its raw duration directly
        duration = round(time.time() - session.start_path_time, 2)
    except AttributeError:
        # High-precision fallback using the terminal reporter's baseline tracking array
        session_start_time = getattr(reporter, "_session_start", getattr(reporter, "_sessionstarttime", None))
        if session_start_time and hasattr(session_start_time, "timestamp"):
            duration = round(time.time() - session_start_time.timestamp(), 2)
        elif isinstance(session_start_time, (int, float)):
            duration = round(time.time() - session_start_time, 2)
        else:
            duration = "N/A"
    
    # 2. Determine execution health status and color themes
    if failed > 0:
        status_title = "🚨 AUTOMATION SUITE FAILURE"
        embed_color = 15158332  # Vivid Red hex code integer
    else:
        status_title = "✅ AUTOMATION SUITE PASS"
        embed_color = 3066993   # Vivid Green hex code integer

    # 3. Construct a standard rich webhook payload structure (Discord Embed Format)
    payload = {
        "embeds": [{
            "title": status_title,
            "description": f"Framework verification pass finished in **{duration}s**.",
            "color": embed_color,
            "fields": [
                {"name": "Total Run", "value": str(total), "inline": True},
                {"name": "Passed ✅", "value": str(passed), "inline": True},
                {"name": "Failed ❌", "value": str(failed), "inline": True},
                {"name": "Skipped 🟡", "value": str(skipped), "inline": True}
            ],
            "footer": {
                "text": "Repository: advanced-pytest-framework | Continuous Integration Core"
            }
        }]
    }

    # 4. Dispatch the HTTP POST payload safely without adding external dependencies
    # Extract webhook URL from environment variables for high security
    webhook_url = os.environ.get("TEAMS_WEBHOOK_URL", "https://httpbin.org")
    
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            webhook_url, 
            data=data, 
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as response:
            # Let the payload stream out safely
            pass
    except Exception:
         # Prevent any network drops from hard-crashing your core testing suites
        pass