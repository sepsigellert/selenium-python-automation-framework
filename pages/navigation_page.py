from selenium.webdriver.common.by import By

class NavigationPage:
    def __init__(self, driver):
        self.driver = driver
        self.menu_link = (By.LINK_TEXT, "Events")
        self.heading = (By.TAG_NAME, "h1")

    def go_to_events(self):
        self.driver.find_element(*self.menu_link).click()

    def get_heading(self):
        return self.driver.find_element(*self.heading).text