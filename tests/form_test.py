from pages.form_page import FormPage

def test_form_submit(driver):
    driver.get("https://example.com/form")  # Replace with your form URL
    form = FormPage(driver)

    form.fill_input("Hello Selenium")
    form.submit_form()

    result = form.get_result()
    assert "Hello Selenium" in result