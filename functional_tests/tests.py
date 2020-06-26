import time

import pytest
from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.common.keys import Keys

MAX_WAIT = 10


@pytest.fixture(scope="session")
def browser_factory():
    """A factory which returns new firefox browsers to use during tests."""
    browsers = []

    def browser_factory():
        browser = webdriver.Firefox()
        browsers.append(browser)
        return browser

    yield browser_factory

    for browser in browsers:
        browser.quit()


def wait_for_row_in_todo_table(text, browser):
    """
    A function which checks if a row with the given text is in the to-do list
    table.
    """
    start = time.time()
    while True:
        try:
            table = browser.find_element_by_id("to-do_items")
            rows = table.find_elements_by_tag_name("tr")
            assert text in [row.text for row in rows]
            return
        except (AssertionError, selenium_exceptions.WebDriverException):
            if time.time() - start > MAX_WAIT:
                raise
            time.sleep(0.5)


def test_can_start_a_list_for_one_user(browser_factory, live_server):
    # Edith has heard about a cool new online to-do app. She goes to check out its homepage.
    browser = browser_factory()

    browser.get(live_server.url)

    # She notices the page title and header mention to-do lists.
    assert "To-Do" in browser.title
    header_text = browser.find_element_by_tag_name("h1").text
    assert "To-Do" in header_text

    # She is invited to enter a to-do item straight away.
    input_ = browser.find_element_by_id("new_item_input")
    assert input_.get_attribute("placeholder") == "Enter a to-do item"

    # She types "Buy peacock feathers" into a text box (Edith's hobby is tying fly-fishing lures).
    input_.send_keys("Buy peacock feathers")

    # When she hits enter, the page updates, and now the page lists "1: Buy peacock feathers" as an item in a to-do
    # list.
    input_.send_keys(Keys.ENTER)

    wait_for_row_in_todo_table("1: Buy peacock feathers", browser)

    # There is a still a text box inviting her to add another item. She enters "Use peacock feathers to make a fly"
    # (Edith is very methodical).
    input_ = browser.find_element_by_id("new_item_input")
    input_.send_keys("Use peacock feathers to make a fly")

    # The page updates again, and now shows both items on her list.
    input_.send_keys(Keys.ENTER)
    time.sleep(1)

    wait_for_row_in_todo_table("1: Buy peacock feathers", browser)
    wait_for_row_in_todo_table("2: Use peacock feathers to make a fly", browser)

    # Edith wonders whether the site will remember her list. Then she sees that the site has generated a unique URL for
    # her - there is some explanatory text to that affect.
    assert 0, "finish this test"

    # She visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep.
