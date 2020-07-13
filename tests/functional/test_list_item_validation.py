from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def test_cannot_add_empty_list_items(selenium, base_url, wait_for, row_in_todo_table, get_item_input):
    # Edith goes to the home page and accidentally tries to submit an empty list
    # item. She hints Enter on the empty input box
    selenium.get(base_url)
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
    selenium: webdriver.Firefox, base_url, get_item_input, wait_for, row_in_todo_table
):
    # Alice goes to the home page and enters a list item
    selenium.get(base_url)
    get_item_input().send_keys("Buy milk", Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")

    # She then enters the same item again without thinking
    get_item_input().send_keys("Buy milk", Keys.ENTER)

    # The page refreshes and an error is shown below the text input saying that
    # duplicate items are not allowed.
    wait_for(lambda: selenium.find_element_by_class_name("is-danger").text == "You can't save a duplicate item")
    assert not row_in_todo_table("2: Buy milk")
