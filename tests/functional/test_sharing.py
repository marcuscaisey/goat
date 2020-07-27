def test_can_share_a_list_with_another_user(browser, base_url, force_login, user, add_list_item):
    # Edith is a logged-in user
    force_login(user)
    browser.get(base_url)

    # Edith goes to the home page and starts a list
    add_list_item("Get help")

    # She notices a "Share this list" option
    share_box = browser.find_element_by_css_selector("input[name=sharee]")
    assert share_box.get_attribute("placeholder") == "your-friend@example.com"
