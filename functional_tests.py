import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope="session")
def browser():
    """A firefox browser to use during tests."""
    browser = webdriver.Firefox()
    yield browser
    browser.quit()


@pytest.fixture
def assert_row_in_todo_table(browser):
    """
    A function which checks if a row with the given text is in the to-do list
    table.
    """

    def assert_row_in_todo_table(text):
        table = browser.find_element_by_id("to-do_items")
        rows = table.find_elements_by_tag_name("tr")
        assert text in [row.text for row in rows]

    return assert_row_in_todo_table


def test_can_start_a_list_and_retrieve_it_later(browser, live_server, assert_row_in_todo_table):
    # Edith has heard about a cool new online to-do app. She goes to check out its homepage.
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
    time.sleep(1)

    assert_row_in_todo_table("1: Buy peacock feathers")

    # There is a still a text box inviting her to add another item. She enters "Use peacock feathers to make a fly"
    # (Edith is very methodical).
    input_ = browser.find_element_by_id("new_item_input")
    input_.send_keys("Use peacock feathers to make a fly")

    # The page updates again, and now shows both items on her list.
    input_.send_keys(Keys.ENTER)
    time.sleep(1)

    assert_row_in_todo_table("1: Buy peacock feathers")
    assert_row_in_todo_table("2: Use peacock feathers to make a fly")

    # Edith wonders whether the site will remember her list. Then she sees that the site has generated a unique URL for
    # her - there is some explanatory text to that affect.
    assert 0, "finish this test"

    # She visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep.
