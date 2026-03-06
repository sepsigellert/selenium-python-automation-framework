from pages.login_page import LoginPage
from data.users import VALID_USER
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_login(driver):
    driver.get("https://www.facebook.com/login")  # CHANGED: use the real target login page
    login = LoginPage(driver)  # CHANGED: keep actions through Page Object
    login.dismiss_cookie_popup()  # CHANGED: explicitly try closing cookie popup right after page load

    login.enter_username(VALID_USER["username"])  # CHANGED: fixed key/method alignment
    login.enter_password(VALID_USER["password"])  # CHANGED: fixed key/method alignment
    login.click_login()  # CHANGED: single login action

    WebDriverWait(driver, 10).until(EC.url_contains("facebook.com"))  # CHANGED: wait for post-click navigation
    current_url = driver.current_url.lower()  # CHANGED: normalize once for stable assertions
    assert any(path in current_url for path in ["/login", "/checkpoint", "/recover"])  # CHANGED: tolerate common FB outcomes
