from pages.navigation_page import NavigationPage

def test_navigation(driver):
    driver.get("https://example.com")  # Replace with your site URL
    nav = NavigationPage(driver)

    nav.go_to_events()
    heading = nav.get_heading()

    assert "Events" in heading