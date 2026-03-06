from pages.form_page import FormPage

def test_form_submit(driver):
    # SAME: You are testing the login page
    driver.get("https://the-internet.herokuapp.com/login")

    form = FormPage(driver)

    # CHANGED: The login page requires BOTH username and password.
    # But your FormPage only supports username for now.
    # So we test only the username field and submit.
    form.fill_input("tomsmith")  # valid username for this site

    # CHANGED: The site requires a password, so we must enter it manually here.
    driver.find_element("id", "password").send_keys("SuperSecretPassword!")

    form.submit_form()

    # UPDATED: The result message appears in the flash element
    result = form.get_result()

    # UPDATED: The success message contains "You logged into a secure area!"
    assert "You logged into a secure area!" in result
