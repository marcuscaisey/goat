def test_logged_in_users_lists_are_saved_in_my_lists(  # noqa: E302
    browser, user, force_login, base_url, wait_for, field, add_list_item
):
    # Edith is a logged in user
    force_login(user)

    # She goes to the home page and starts a list
    browser.get(base_url)
    add_list_item("oat milk")
    add_list_item("oats")
    first_list_url = browser.current_url

    # She notices a "My lists" link, for the firs time
    browser.find_element_by_link_text("My lists").click()

    # She see that her list is in there, named accordingly to its first item
    wait_for(lambda: browser.find_element_by_link_text("oat milk"))
    browser.find_element_by_link_text("oat milk").click()
    wait_for(lambda: browser.current_url == first_list_url)

    # She then decides to make another list
    browser.get(base_url)
    add_list_item("click cows")
    second_list_url = browser.current_url

    # Under "My lists", her new list appears
    browser.find_element_by_link_text("My lists").click()
    wait_for(lambda: browser.find_element_by_link_text("click cows"))
    browser.find_element_by_link_text("click cows").click()
    wait_for(lambda: browser.current_url == second_list_url)

    # She logs out and the "My lists" link disappears
    browser.find_element_by_link_text("Logout").click()
    wait_for(lambda: not browser.find_elements_by_link_text("My lists"))
