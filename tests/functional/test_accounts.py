import pytest
from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions


def test_can_log_in(selenium: webdriver.Firefox, base_url, user, wait_for):
    # A user who has an account goes to the home page
    selenium.get(base_url)

    # They click the link to the login page
    selenium.find_element_by_link_text("Login").click()

    # They input their email and password and click login
    selenium.find_element_by_id("id_username").send_keys(user.email)
    selenium.find_element_by_id("id_password").send_keys(user.password)
    selenium.find_element_by_css_selector("input[type=submit]").click()

    # The user is now logged in and redirected back to the home page
    wait_for(lambda: selenium.find_element_by_link_text("Logout"))
    with pytest.raises(selenium_exceptions.NoSuchElementException):
        selenium.find_element_by_link_text("Login")
    assert selenium.current_url == base_url
    assert selenium.find_element_by_id("logged_in_user").text == user.email
