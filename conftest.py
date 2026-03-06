import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    ChromeDriverManager = None


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")

    # CI-only flags (GitHub Actions)
    if os.getenv("GITHUB_ACTIONS") == "true":
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    # Use webdriver_manager if available, otherwise Selenium Manager fallback
    if ChromeDriverManager is not None:
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=options)
    else:
        browser = webdriver.Chrome(options=options)

    browser.implicitly_wait(5)
    yield browser

    # Take screenshot on failure
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        screenshots_dir = os.path.join(os.path.dirname(__file__), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        browser.save_screenshot(os.path.join(screenshots_dir, f"{request.node.name}.png"))

    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    _ = call.when
    outcome = yield
    report = outcome.get_result()
    if "driver" in item.fixturenames:
        setattr(item, "rep_" + report.when, report)
