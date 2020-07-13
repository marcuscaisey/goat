import re

from selenium.webdriver.common.keys import Keys


def test_can_start_a_list_for_one_user(selenium, base_url, wait_for, row_in_todo_table, get_item_input):
    # Edith has heard about a cool new online to-do app. She goes to check out its homepage.
    selenium.get(base_url)

    # She notices the page title and header mention to-do lists.
    assert "To-Do" in selenium.title
    header_text = selenium.find_element_by_tag_name("h1").text
    assert "To-Do" in header_text

    # She is invited to enter a to-do item straight away.
    input_ = get_item_input()
    assert input_.get_attribute("placeholder") == "Enter a to-do item"

    # She types "Buy peacock feathers" into a text box (Edith's hobby is tying fly-fishing lures).
    input_.send_keys("Buy peacock feathers")

    # When she hits enter, the page updates, and now the page lists "1: Buy peacock feathers" as an item in a to-do
    # list.
    input_.send_keys(Keys.ENTER)

    wait_for(row_in_todo_table, "1: Buy peacock feathers")

    # There is a still a text box inviting her to add another item. She enters "Use peacock feathers to make a fly"
    # (Edith is very methodical).
    input_ = get_item_input()
    input_.send_keys("Use peacock feathers to make a fly")

    # The page updates again, and now shows both items on her list.
    input_.send_keys(Keys.ENTER)

    wait_for(row_in_todo_table, "1: Buy peacock feathers")
    wait_for(row_in_todo_table, "2: Use peacock feathers to make a fly")

    # Satisfied, she goes back to sleep.


def test_multiple_users_can_start_lists_at_different_urls(
    selenium, base_url, wait_for, row_in_todo_table, get_item_input
):
    lists_url_pattern = r"/lists/.+"

    # Edith start a new to-do list
    selenium.get(base_url)
    input_ = get_item_input()
    input_.send_keys("Buy peacock feathers")
    input_.send_keys(Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy peacock feathers")

    # She notices that her list has a new URL
    edith_list_url = selenium.current_url
    assert re.search(lists_url_pattern, edith_list_url)

    # Edith is done with her to-do list for now

    # Now a new user, Francis, comes along to the site

    # Francis visits the home page. There's no sign of Edith's list
    selenium.get(base_url)
    page_text = selenium.find_element_by_tag_name("body").text
    assert "Buy peacock feathers" not in page_text

    # Francis starts a new list by entering a new item. He is less interesting
    # than Edith...
    input_ = get_item_input()
    input_.send_keys("Buy milk")
    input_.send_keys(Keys.ENTER)
    wait_for(row_in_todo_table, "1: Buy milk")

    # Francis gets his own unique URL
    francis_list_url = selenium.current_url
    assert re.search(lists_url_pattern, francis_list_url)
    assert francis_list_url != edith_list_url

    # Again, there is no trace of Edith's list
    page_text = selenium.find_element_by_tag_name("body").text
    assert "Buy peacock feathers" not in page_text

    # Francis is done for now as well
