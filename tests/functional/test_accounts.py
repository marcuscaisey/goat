from selenium import webdriver


def test_can_log_in(selenium: webdriver.Firefox, base_url, user, wait_for):
    # A user who has an account goes to the home page
    selenium.get(base_url)

    # They input their username and password into the username and password
    # fields at the top of the page and click login
    selenium.find_element_by_id("id_username").send_keys(user.username)
    selenium.find_element_by_id("id_password").send_keys(user.password)
    selenium.find_element_by_id("login").click()

    # The user is now logged in
    wait_for(lambda: selenium.find_element_by_id("logout"))
    assert selenium.find_element_by_id("logged_in_user") == user.username
    assert not selenium.find_element_by_id("id_username")
    assert not selenium.find_element_by_id("id_password")
