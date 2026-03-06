from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NavigationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # Locators
    IPHONE_BUTTON = (By.CSS_SELECTOR, "a.globalnav-link[href='/iphone/']")
    APPLE_LOGO = (By.CSS_SELECTOR, "a.globalnav-link-apple")
    COOKIE_BANNER = (By.ID, "ac-ls-cc-accept")

    def open_homepage(self):
        self.driver.get("https://www.apple.com/")
        self._handle_cookie_banner()

    def _handle_cookie_banner(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.COOKIE_BANNER))
            btn.click()
        except Exception:
            pass

    def click_iphone(self):
        # Click the iPhone link
        self.wait.until(EC.element_to_be_clickable(self.IPHONE_BUTTON)).click()

        # Wait for URL to confirm page load
        self.wait.until(EC.url_contains("/iphone"))

    def go_home(self):
        self.wait.until(EC.element_to_be_clickable(self.APPLE_LOGO)).click()
        self.wait.until(EC.url_to_be("https://www.apple.com/"))

    def get_current_url(self):
        return self.driver.current_url
