import pytest
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.common.keys import Keys


def test_can_log_in(browser, home_url, user, wait_for, field):
    # A user who has an account goes to the home page, they can see that they're
    # not logged in
    browser.get(home_url)
    with pytest.raises(selenium_exceptions.NoSuchElementException):
        browser.find_element_by_id("logged_in_user")

    # They click the link to the login page
    browser.find_element_by_link_text("Login").click()

    # They input their email and password and click login
    field("username").send_keys(user.email)
    field("password").send_keys(user.raw_password, Keys.ENTER)

    # The user is now logged in and redirected back to the home page
    wait_for(lambda: browser.find_element_by_link_text("Logout"))
    with pytest.raises(selenium_exceptions.NoSuchElementException):
        browser.find_element_by_link_text("Login")
    assert browser.current_url == home_url
    assert browser.find_element_by_id("logged-in-user").text == user.email


def test_login_failure_shows_error_message(browser, login_url, user, wait_for):
    # A user goes to the login page
    browser.get(login_url)

    # They enter their password in incorrectly
    browser.find_element_by_id("id_username").send_keys(user.email)
    browser.find_element_by_id("id_password").send_keys("incorrect-" + user.raw_password)
    browser.find_element_by_css_selector("input[type=submit]").click()

    # The user is sent back to the login page
    wait_for(lambda: browser.current_url == login_url)

    # There's a message explaining the error on the page now
    assert (
        browser.find_element_by_css_selector(".notification.is-danger").text
        == "The email address and password provided do not match any of our records."
    )


def test_can_log_out(browser, home_url, user, wait_for, force_login):
    # A user has logged themselves in and gone to the home page
    force_login(user)
    browser.get(home_url)

    # They now want to log out, so they click the link to logout
    browser.find_element_by_link_text("Logout").click()

    # They're logged out and sent back to the home page
    wait_for(lambda: browser.find_element_by_link_text("Login"))
    assert browser.current_url == home_url


def test_can_sign_up(browser, home_url, login_url, wait_for, client, valid_email, valid_password):
    # A user wants to create an account, so they go to the home page and click
    # the Signup link
    browser.get(home_url)
    browser.find_element_by_link_text("Signup").click()

    # They enter their email and password and click the Sign Up button
    browser.find_element_by_id("id_email").send_keys(valid_email)
    browser.find_element_by_id("id_password1").send_keys(valid_password)
    browser.find_element_by_id("id_password2").send_keys(valid_password)
    browser.find_element_by_css_selector("input[type=submit]").click()

    # The user's account has now been created and they are redirected to the
    # login page
    wait_for(lambda: browser.current_url == login_url)
    assert client.login(username=valid_email, password=valid_password)


@pytest.fixture
def fill_signup_with_valid_input(browser, field, valid_email, valid_password):
    def fill_signup_with_valid_input(exclude=()):
        values = {"email": valid_email, "password1": valid_password, "password2": valid_password}
        for name, value in values.items():
            field(name).clear()
            if name not in exclude:
                field(name).send_keys(value)

    return fill_signup_with_valid_input


def test_signup_field_errors_show_error_messages(
    browser,
    signup_url,
    field,
    field_error,
    wait_for,
    user,
    invalid_email,
    short_password,
    numeric_password,
    valid_password,
    fill_signup_with_valid_input,
):
    # A user wants to create an account, so they go to the signup page
    browser.get(signup_url)

    # They unluckily go through a series of invalid email and password
    # combinations which result in error messages being shown below the invalid
    # fields

    # First they try an invalid email
    fill_signup_with_valid_input(exclude=["email"])
    field("email").send_keys(invalid_email, Keys.ENTER)
    wait_for(lambda: browser.find_element_by_css_selector("#id_email:invalid"))

    # First they try and email that has already been used
    fill_signup_with_valid_input(exclude=["email"])
    field("email").send_keys(user.email, Keys.ENTER)
    wait_for(lambda: field_error("email").text == "A user with this email address already exists.")

    # Then they try entering a password which is too short
    fill_signup_with_valid_input(exclude=["password1", "password2"])
    field("password1").send_keys(short_password)
    field("password2").send_keys(short_password, Keys.ENTER)
    wait_for(
        lambda: field_error("password2").text == "This password is too short. It must contain at least 10 characters."
    )

    # Then they try a password which is entirely numeric
    fill_signup_with_valid_input(exclude=["password1", "password2"])
    field("password1").send_keys(numeric_password)
    field("password2").send_keys(numeric_password, Keys.ENTER)
    wait_for(lambda: field_error("password2").text == "This password is entirely numeric.")

    # Finally, they accidentally type different passwords into the fields
    fill_signup_with_valid_input(exclude=["password1", "password2"])
    field("password1").send_keys(valid_password)
    field("password2").send_keys("incorrect" + valid_password, Keys.ENTER)
    wait_for(lambda: field_error("password2").text == "This password doesn't match the one entered before.")
