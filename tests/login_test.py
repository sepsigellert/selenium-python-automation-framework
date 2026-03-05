from pages.login_page import LoginPage

def test_login(driver):
    driver.get("https://example.com/login")  # Replace with your login URL
    login = LoginPage(driver)

    login.enter_username("testuser")
    login.enter_password("password")
    login.click_login()

    assert "Dashboard" in driver.title