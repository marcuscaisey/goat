import re

from selenium.webdriver.common.keys import Keys


def test_can_start_a_list_for_one_user(browser, live_server_url, wait_for_row_in_todo_table, get_item_input):
    # Edith has heard about a cool new online to-do app. She goes to check out its homepage.
    browser.get(live_server_url)

    # She notices the page title and header mention to-do lists.
    assert "To-Do" in browser.title
    header_text = browser.find_element_by_tag_name("h1").text
    assert "To-Do" in header_text

    # She is invited to enter a to-do item straight away.
    input_ = get_item_input(browser)
    assert input_.get_attribute("placeholder") == "Enter a to-do item"

    # She types "Buy peacock feathers" into a text box (Edith's hobby is tying fly-fishing lures).
    input_.send_keys("Buy peacock feathers")

    # When she hits enter, the page updates, and now the page lists "1: Buy peacock feathers" as an item in a to-do
    # list.
    input_.send_keys(Keys.ENTER)

    wait_for_row_in_todo_table("1: Buy peacock feathers", browser)

    # There is a still a text box inviting her to add another item. She enters "Use peacock feathers to make a fly"
    # (Edith is very methodical).
    input_ = get_item_input(browser)
    input_.send_keys("Use peacock feathers to make a fly")

    # The page updates again, and now shows both items on her list.
    input_.send_keys(Keys.ENTER)

    wait_for_row_in_todo_table("1: Buy peacock feathers", browser)
    wait_for_row_in_todo_table("2: Use peacock feathers to make a fly", browser)

    # Satisfied, she goes back to sleep.


def test_multiple_users_can_start_lists_at_different_urls(
    browser_factory, live_server_url, wait_for_row_in_todo_table, get_item_input
):
    lists_url_pattern = r"/lists/.+"

    # Edith start a new to-do list
    edith_browser = browser_factory()

    edith_browser.get(live_server_url)
    input_ = get_item_input(edith_browser)
    input_.send_keys("Buy peacock feathers")
    input_.send_keys(Keys.ENTER)
    wait_for_row_in_todo_table("1: Buy peacock feathers", edith_browser)

    # She notices that her list has a new URL
    edith_list_url = edith_browser.current_url
    assert re.search(lists_url_pattern, edith_list_url)

    # Edith is done with her to-do list for now

    # Now a new user, Francis, comes along to the site
    francis_browser = browser_factory()

    # Francis visits the home page. There's no sign of Edith's list
    francis_browser.get(live_server_url)
    page_text = francis_browser.find_element_by_tag_name("body").text
    assert "Buy peacock feathers" not in page_text

    # Francis starts a new list by entering a new item. He is less interesting
    # than Edith...
    input_ = get_item_input(francis_browser)
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
