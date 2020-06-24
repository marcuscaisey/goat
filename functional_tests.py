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


def test_can_start_a_list_and_retrieve_it_later(browser: webdriver.Remote, live_server):
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

    table = browser.find_element_by_id("to-do_items")
    rows = table.find_elements_by_tag_name("tr")
    assert any(row.text == "1: Buy peacock feathers" for row in rows)

    # There is a still a text box inviting her to add another item. She enters "Use peacock feathers to make a fly"
    # (Edith is very methodical).
    assert 0, "not finished"

    # The page updates again, and now shows both items on her list.

    # Edith wonders whether the site will remember her list. Then she sees that the site has generated a unique URL for
    # her - there is some explanatory text to that affect.

    # She visits that URL - her to-do list is still there.

    # Satisfied, she goes back to sleep.
