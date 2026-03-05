import pytest
from selenium import webdriver
import os

@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    yield driver

    # Take screenshot on failure
    # if request.node.rep_call.failed:  # CHANGED: old direct access could fail if rep_call is missing/invalid
    rep = getattr(request.node, "rep_call", None)  # CHANGED: safely read rep_call from the test node
    if rep and rep.failed:  # CHANGED: guard check avoids AttributeError and then verifies test failure
        os.makedirs("screenshots", exist_ok=True)  # CHANGED: keep creating screenshots folder when needed
        driver.save_screenshot(f"screenshots/{request.node.name}.png")  # CHANGED: keep screenshot naming behavior

    driver.quit()


# Hook to capture test outcome
# def pytest_runtest_makereport(item, call):  # CHANGED: old hook saved CallInfo, not TestReport
#     if "driver" in item.fixturenames:  # CHANGED: old conditional left for reference
#         setattr(item, "rep_" + call.when, call)  # CHANGED: old assignment caused `.failed` AttributeError
@pytest.hookimpl(hookwrapper=True)  # CHANGED: enable wrapper so we can access the generated TestReport
def pytest_runtest_makereport(item, call):  # CHANGED: keep same hook name with corrected implementation
    outcome = yield  # CHANGED: run the actual pytest hook chain first
    report = outcome.get_result()  # CHANGED: extract TestReport object (has `.failed`)
    if "driver" in item.fixturenames:  # CHANGED: keep behavior scoped to tests using the driver fixture
        setattr(item, "rep_" + report.when, report)  # CHANGED: store TestReport instead of CallInfo
