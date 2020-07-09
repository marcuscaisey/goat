import pytest
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.common.keys import Keys


def test_cannot_add_empty_list_items(browser, live_server_url, wait_for, wait_for_row_in_todo_table):
    # Edith goes to the home page and accidentally tries to submit an empty list
    # item. She hints Enter on the empty input box
    browser.get(live_server_url)
    browser.find_element_by_id("new_item_input").send_keys(Keys.ENTER)

    # The home page refreshes and there is an error message saying that list
    # items cannot be blank
    wait_for(lambda: browser.find_element_by_css_selector(".is-danger").text == "You can't have an empty list item")

    # She tries again with some text for the item, which now works
    browser.find_element_by_id("new_item_input").send_keys("Buy milk", Keys.ENTER)
    wait_for_row_in_todo_table("1. Buy milk", browser)
    with pytest.raises(selenium_exceptions.NoSuchElementException):
        browser.find_element_by_css_selector(".is-danger")

    # Perversely, she now decides to submit a second blank list item
    browser.find_element_by_id("new_item_input").send_keys(Keys.ENTER)

    # She receives a similar warning on the list page
    wait_for(lambda: browser.find_element_by_css_selector(".is-danger").text == "You can't have an empty list item")

    # And she can correct it by filling some text in
    browser.find_element_by_id("new_item_input").send_keys("Make tea", Keys.ENTER)
    wait_for_row_in_todo_table("1. Buy milk", browser)
    wait_for_row_in_todo_table("2. Make tea", browser)
    with pytest.raises(selenium_exceptions.NoSuchElementException):
        browser.find_element_by_css_selector(".is-danger")
