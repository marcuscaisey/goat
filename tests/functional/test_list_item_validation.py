from selenium.webdriver.common.keys import Keys


def test_cannot_add_empty_list_items(selenium, live_server_url, wait_for, wait_for_row_in_todo_table, get_item_input):
    # Edith goes to the home page and accidentally tries to submit an empty list
    # item. She hints Enter on the empty input box
    selenium.get(live_server_url)
    get_item_input(selenium).send_keys(Keys.ENTER)

    # The home page refreshes and there is an error message saying that list
    # items cannot be blank
    wait_for(lambda: selenium.find_element_by_css_selector("#id_text:invalid"))

    # She tries again with some text for the item, which now works
    get_item_input(selenium).send_keys("Buy milk", Keys.ENTER)
    wait_for_row_in_todo_table("1: Buy milk", selenium)

    # Perversely, she now decides to submit a second blank list item
    get_item_input(selenium).send_keys(Keys.ENTER)

    # She receives a similar warning on the list page
    wait_for(lambda: selenium.find_element_by_css_selector("#id_text:invalid"))

    # And she can correct it by filling some text in
    get_item_input(selenium).send_keys("Make tea", Keys.ENTER)
    wait_for_row_in_todo_table("1: Buy milk", selenium)
    wait_for_row_in_todo_table("2: Make tea", selenium)
