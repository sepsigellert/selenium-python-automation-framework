from pages.navigation_page import NavigationPage


def test_navigation(driver):
    nav = NavigationPage(driver)

    nav.open_homepage()
    assert "apple.com" in nav.get_current_url()

    nav.click_iphone()
    assert "/iphone" in nav.get_current_url()

    nav.go_home()
    assert nav.get_current_url().rstrip("/") == "https://www.apple.com"
