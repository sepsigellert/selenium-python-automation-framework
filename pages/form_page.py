from selenium.webdriver.common.by import By

class FormPage:
    def __init__(self, driver):
        self.driver = driver

        # CHANGED: The Herokuapp login page does NOT have "input-field".
        # It has an input with id="username".
        self.username_field = (By.ID, "username")

        # CHANGED: The login button is NOT an <input>. It is a <button>.
        # Correct selector:
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")

        # CHANGED: The page does NOT have an element with id="result".
        # After login, the success message appears in a div with id="flash".
        self.result_text = (By.ID, "flash")

    def fill_input(self, text):
        # UPDATED: Use the correct username field
        self.driver.find_element(*self.username_field).clear()
        self.driver.find_element(*self.username_field).send_keys(text)

    def submit_form(self):
        # UPDATED: Click the correct button
        self.driver.find_element(*self.submit_button).click()

    def get_result(self):
        # UPDATED: Return the flash message text
        return self.driver.find_element(*self.result_text).text
