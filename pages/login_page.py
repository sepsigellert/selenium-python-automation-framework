from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # CHANGED: allow Enter-key submit fallback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException  # CHANGED: handle blocked/overlay clicks

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # CHANGED: use one explicit wait object for all interactions
        self.short_wait = WebDriverWait(driver, 3)  # CHANGED: shorter wait for optional popup checks
        self.email_locators = [  # CHANGED: support desktop + mobile Facebook login variants
            (By.ID, "email"),
            (By.NAME, "email"),
            (By.ID, "m_login_email"),
        ]
        self.password_locators = [  # CHANGED: support desktop + mobile Facebook login variants
            (By.ID, "pass"),
            (By.NAME, "pass"),
            (By.ID, "m_login_password"),
        ]
        self.login_locators = [  # CHANGED: support desktop + mobile Facebook login variants
            (By.NAME, "login"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "input[type='submit']"),
        ]
        self.cookie_buttons = [  # CHANGED: broaden popup locator strategies (text + attributes)
            (By.XPATH, "//button[contains(., 'Allow all cookies')]"),
            (By.XPATH, "//button[contains(., 'Accept all')]"),
            (By.XPATH, "//*[@role='button' and contains(., 'Allow all cookies')]"),
            (By.XPATH, "//*[@role='button' and contains(., 'Accept all')]"),
            (By.CSS_SELECTOR, "button[data-cookiebanner='accept_button']"),
            (By.CSS_SELECTOR, "[aria-label='Allow all cookies']"),
        ]

    def _first_visible(self, locators):  # CHANGED: helper to pick first visible element from multiple locators
        for locator in locators:
            try:
                return self.short_wait.until(EC.visibility_of_element_located(locator))
            except TimeoutException:
                continue
        return self.wait.until(EC.visibility_of_element_located(locators[0]))  # CHANGED: raise clear TimeoutException if none found

    def _first_clickable(self, locators):  # CHANGED: helper to pick first clickable element from multiple locators
        for locator in locators:
            try:
                return self.short_wait.until(EC.element_to_be_clickable(locator))
            except TimeoutException:
                continue
        return self.wait.until(EC.element_to_be_clickable(locators[0]))  # CHANGED: raise clear TimeoutException if none found

    def _first_present(self, locators):  # CHANGED: helper to pick first present element for JS fallback clicks
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            if elements:
                return elements[0]
        return None

    def dismiss_cookie_popup(self):  # CHANGED: public method so tests can call it explicitly
        for locator in self.cookie_buttons:
            try:
                self.short_wait.until(EC.element_to_be_clickable(locator)).click()  # CHANGED: do not block test flow for long
                return True  # CHANGED: report successful popup close
            except (TimeoutException, ElementClickInterceptedException):  # CHANGED: keep trying alternative locators
                continue
        return False  # CHANGED: explicit "not found/not closed" status

    def enter_username(self, email):
        self.dismiss_cookie_popup()  # CHANGED: keep defensive popup close in page object too
        field = self._first_visible(self.email_locators)  # CHANGED: robust locator resolution for email field
        field.clear()
        field.send_keys(email)

    def enter_password(self, password):
        field = self._first_visible(self.password_locators)  # CHANGED: robust locator resolution for password field
        field.clear()
        field.send_keys(password)

    def click_login(self):
        self.dismiss_cookie_popup()  # CHANGED: retry popup close before submit in case overlay reappears
        try:
            self._first_clickable(self.login_locators).click()  # CHANGED: primary path uses normal user click
            return
        except TimeoutException:
            pass  # CHANGED: continue with fallbacks when clickable button cannot be reached

        button = self._first_present(self.login_locators)  # CHANGED: fallback to JS click on present button
        if button is not None:
            self.driver.execute_script("arguments[0].click();", button)
            return

        self._first_visible(self.password_locators).send_keys(Keys.ENTER)  # CHANGED: final fallback submits form via Enter
