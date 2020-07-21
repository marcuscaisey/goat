import pytest
from selenium.common import exceptions as selenium_exceptions


def test_can_log_in(selenium, home_url, user, wait_for):
    # A user who has an account goes to the home page, they can see that they're
    # not logged in
    selenium.get(home_url)
    with pytest.raises(selenium_exceptions.NoSuchElementException):
        selenium.find_element_by_id("logged_in_user")

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
    assert selenium.current_url == home_url
    assert selenium.find_element_by_id("logged-in-user").text == user.email


def test_login_failure_shows_error_message(selenium, login_url, user, wait_for):
    # A user goes to the login page
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


def test_can_log_out(selenium, home_url, user, wait_for, force_login):
    # A user has logged themselves in and gone to the home page
    force_login(user)
    selenium.get(home_url)

    # They now want to log out, so they click the link to logout
    selenium.find_element_by_link_text("Logout").click()

    # They're logged out and sent back to the home page
    wait_for(lambda: selenium.find_element_by_link_text("Login"))
    assert selenium.current_url == home_url


def test_can_sign_up(selenium, home_url, login_url, wait_for, client, valid_email, valid_password):
    # A user wants to create an account, so they go to the home page and click
    # the Signup link
    selenium.get(home_url)
    selenium.find_element_by_link_text("Signup").click()

    # They enter their email and password and click the Sign Up button
    selenium.find_element_by_id("id_email").send_keys(valid_email)
    selenium.find_element_by_id("id_password1").send_keys(valid_password)
    selenium.find_element_by_id("id_password2").send_keys(valid_password)
    selenium.find_element_by_css_selector("input[type=submit]").click()

    # The user's account has now been created and they are redirected to the
    # login page
    wait_for(lambda: selenium.current_url == login_url)
    assert client.login(username=valid_email, password=valid_password)
