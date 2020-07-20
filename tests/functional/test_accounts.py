import pytest
from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions


def test_can_log_in(selenium: webdriver.Firefox, base_url, user, wait_for):
    # A user who has an account goes to the home page, they can see that they're
    # not logged in
    selenium.get(base_url)
    with pytest.raises(selenium_exceptions.NoSuchElementException):
        assert selenium.find_element_by_id("logged_in_user").text == user.email

    # They click the link to the login page
    selenium.find_element_by_link_text("Login").click()

    # They input their email and password and click login
    selenium.find_element_by_id("id_username").send_keys(user.email)
    selenium.find_element_by_id("id_password").send_keys(user.raw_password)
    selenium.find_element_by_css_selector("input[type=submit]").click()

    # The user is now logged in and redirected back to the home page
    wait_for(lambda: selenium.find_element_by_link_text("Logout"))
    with pytest.raises(selenium_exceptions.NoSuchElementException):
        selenium.find_element_by_link_text("Login")
    assert selenium.current_url == base_url
    assert selenium.find_element_by_id("logged-in-user").text == user.email


def test_login_failure_shows_error_message(selenium: webdriver.Firefox, base_url, user, wait_for):
    # A user goes to the login page
    login_url = base_url + "login/"
    selenium.get(login_url)

    # They enter their password in incorrectly
    selenium.find_element_by_id("id_username").send_keys(user.email)
    selenium.find_element_by_id("id_password").send_keys("incorrect-" + user.raw_password)
    selenium.find_element_by_css_selector("input[type=submit]").click()

    # The user is sent back to the login page
    wait_for(lambda: selenium.current_url == login_url)

    # There's a message explaining the error on the page now
    assert (
        selenium.find_element_by_css_selector(".notification.is-danger").text
        == "The email address and password provided do not match any of our records."
    )
