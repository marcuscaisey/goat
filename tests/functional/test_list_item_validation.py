import pytest
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def new_item_error(browser, new_item_input_id):
    """
    A function which gets the error element for the new item input from the
    page.
    """

    def new_item_error():
        return browser.find_element_by_id(f"{new_item_input_id}-error")

    return new_item_error


def test_cannot_add_empty_list_items(browser, home_url, wait_for, row_in_todo_table, new_item_input, new_item_error):
    # Edith goes to the home page and accidentally tries to submit an empty list
    # item. She hints Enter on the empty input box
    browser.get(home_url)
    new_item_input().send_keys(Keys.ENTER)

    # The home page refreshes and there is an error message saying that list
    # items cannot be blank
    wait_for(lambda: browser.find_element_by_css_selector("#id_text:invalid"))

    # She tries again with some text for the item, which now works
    new_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")

    # Perversely, she now decides to submit a second blank list item
    new_item_input().send_keys(Keys.ENTER)

    # She receives a similar warning on the list page
    wait_for(lambda: browser.find_element_by_css_selector("#id_text:invalid"))

    # And she can correct it by filling some text in
    new_item_input().send_keys("Make tea", Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")
    wait_for(row_in_todo_table, "2: Make tea")


def test_cannot_add_duplicate_list_items(
    browser, home_url, new_item_input, wait_for, row_in_todo_table, new_item_error
):
    # Alice goes to the home page and enters a list item
    browser.get(home_url)
    new_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")

    # She then enters the same item again without thinking
    new_item_input().send_keys("Buy milk", Keys.ENTER)

    # The page refreshes and an error is shown below the text input saying that
    # duplicate items are not allowed.
    wait_for(lambda: new_item_error().text == "You can't save a duplicate item")
    assert not row_in_todo_table("2: Buy milk")


def test_error_messages_are_cleared_on_input(
    browser, home_url, wait_for, row_in_todo_table, new_item_input, new_item_error
):
    # Alice starts a list and causes a validation error
    browser.get(home_url)
    new_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")
    new_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(lambda: new_item_error().is_displayed())

    # She starts typing in the input box to clear the error
    new_item_input().send_keys("a")

    # She is pleased to see that the error messages disappears
    wait_for(lambda: not new_item_error().is_displayed())


def test_error_messages_are_cleared_when_input_clicked(
    browser, home_url, wait_for, row_in_todo_table, new_item_input, new_item_error
):
    # Alice starts a list and causes a validation error
    browser.get(home_url)
    new_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")
    new_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(lambda: new_item_error().is_displayed())

    # She clicks the input box to clear the error
    new_item_input().click()

    # She is pleased to see that the error messages disappears
    wait_for(lambda: not new_item_error().is_displayed())
