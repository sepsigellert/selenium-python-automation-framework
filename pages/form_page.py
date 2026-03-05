from selenium.webdriver.common.by import By

class FormPage:
    def __init__(self, driver):
        self.driver = driver
        self.input_field = (By.ID, "input-field")
        self.submit_button = (By.CSS_SELECTOR, "input[type='submit']")
        self.result_text = (By.ID, "result")

    def fill_input(self, text):
        self.driver.find_element(*self.input_field).clear()
        self.driver.find_element(*self.input_field).send_keys(text)

    def submit_form(self):
        self.driver.find_element(*self.submit_button).click()

    def get_result(self):
        return self.driver.find_element(*self.result_text).text