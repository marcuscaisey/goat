import os
import re
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


@pytest.fixture(scope="session")
def live_server_url(live_server):
    return os.getenv("STAGING_SERVER", live_server.url)


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


def test_can_start_a_list_for_one_user(browser_factory, live_server_url):
    # Edith has heard about a cool new online to-do app. She goes to check out its homepage.
    browser = browser_factory()

    browser.get(live_server_url)

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

    wait_for_row_in_todo_table("1: Buy peacock feathers", browser)
    wait_for_row_in_todo_table("2: Use peacock feathers to make a fly", browser)

    # Satisfied, she goes back to sleep.
    browser.quit()


def test_multiple_users_can_start_lists_at_different_urls(browser_factory, live_server_url):
    lists_url_pattern = r"/lists/.+"

    # Edith start a new to-do list
    edith_browser = browser_factory()

    edith_browser.get(live_server_url)
    input_ = edith_browser.find_element_by_id("new_item_input")
    input_.send_keys("Buy peacock feathers")
    input_.send_keys(Keys.ENTER)
    wait_for_row_in_todo_table("1: Buy peacock feathers", edith_browser)

    # She notices that her list has a new URL
    edith_list_url = edith_browser.current_url
    assert re.search(lists_url_pattern, edith_list_url)

    # Edith is done with her to-do list for now
    edith_browser.quit()

    # Now a new user, Francis, comes along to the site
    francis_browser = browser_factory()

    # Francis visits the home page. There's no sign of Edith's list
    francis_browser.get(live_server_url)
    page_text = francis_browser.find_element_by_tag_name("body").text
    assert "Buy peacock feathers" not in page_text

    # Francis starts a new list by entering a new item. He is less interesting
    # than Edith...
    input_ = francis_browser.find_element_by_id("new_item_input")
    input_.send_keys("Buy milk")
    input_.send_keys(Keys.ENTER)
    wait_for_row_in_todo_table("1: Buy milk", francis_browser)

    # Francis gets his own unique URL
    francis_list_url = francis_browser.current_url
    assert re.search(lists_url_pattern, francis_list_url)
    assert francis_list_url != edith_list_url

    # Again, there is no trace of Edith's list
    page_text = francis_browser.find_element_by_tag_name("body").text
    assert "Buy peacock feathers" not in page_text

    # Francis is done for now as well
    francis_browser.quit()


def test_layout(browser_factory, live_server_url):
    browser = browser_factory()
    browser.set_window_size(1024, 768)

    browser.get(live_server_url)

    input_ = browser.find_element_by_id("new_item_input")
    assert input_.location["x"] + input_.size["width"] / 2 == pytest.approx(512, abs=10)

    browser.quit()
