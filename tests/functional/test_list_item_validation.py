import pytest
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def get_error_container(selenium):
    """
    A function which gets the container containing the error message from the
    page.
    """

    def get_error_container():
        return selenium.find_element_by_class_name("is-danger")

    return get_error_container


def test_cannot_add_empty_list_items(
    selenium, home_url, wait_for, row_in_todo_table, get_item_input, get_error_container
):
    # Edith goes to the home page and accidentally tries to submit an empty list
    # item. She hints Enter on the empty input box
    selenium.get(home_url)
    get_item_input().send_keys(Keys.ENTER)

    # The home page refreshes and there is an error message saying that list
    # items cannot be blank
    wait_for(lambda: selenium.find_element_by_css_selector("#id_text:invalid"))

    # She tries again with some text for the item, which now works
    get_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")

    # Perversely, she now decides to submit a second blank list item
    get_item_input().send_keys(Keys.ENTER)

    # She receives a similar warning on the list page
    wait_for(lambda: selenium.find_element_by_css_selector("#id_text:invalid"))

    # And she can correct it by filling some text in
    get_item_input().send_keys("Make tea", Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")
    wait_for(row_in_todo_table, "2: Make tea")


def test_cannot_add_duplicate_list_items(
    selenium, home_url, get_item_input, wait_for, row_in_todo_table, get_error_container
):
    # Alice goes to the home page and enters a list item
    selenium.get(home_url)
    get_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")

    # She then enters the same item again without thinking
    get_item_input().send_keys("Buy milk", Keys.ENTER)

    # The page refreshes and an error is shown below the text input saying that
    # duplicate items are not allowed.
    wait_for(lambda: get_error_container().text == "You can't save a duplicate item")
    assert not row_in_todo_table("2: Buy milk")


def test_error_messages_are_cleared_on_input(
    selenium, home_url, wait_for, row_in_todo_table, get_item_input, get_error_container
):
    # Alice starts a list and causes a validation error
    selenium.get(home_url)
    get_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")
    get_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(lambda: get_error_container().is_displayed())

    # She starts typing in the input box to clear the error
    get_item_input().send_keys("a")

    # She is pleased to see that the error messages disappears
    wait_for(lambda: not get_error_container().is_displayed())


def test_error_messages_are_cleared_when_input_clicked(
    selenium, home_url, wait_for, row_in_todo_table, get_item_input, get_error_container
):
    # Alice starts a list and causes a validation error
    selenium.get(home_url)
    get_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")
    get_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(lambda: get_error_container().is_displayed())

    # She clicks the input box to clear the error
    get_item_input().click()

    # She is pleased to see that the error messages disappears
    wait_for(lambda: not get_error_container().is_displayed())
