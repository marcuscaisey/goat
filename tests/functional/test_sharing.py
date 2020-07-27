def test_can_share_a_list_with_another_user(  # noqa: E302
    browser, base_url, force_login, user_factory, list_page, my_lists_page, wait_for
):
    edith = user_factory(email="edith@example.com")
    oni = user_factory(email="oniciferous@example.com")

    # Edith is a logged-in user
    force_login(edith)

    # Edith goes to the home page and starts a list
    browser.get(base_url)
    list_page.add_list_item("Get help")
    list_url = browser.current_url

    # She notices a "Share this list" option
    assert list_page.share_box.get_attribute("placeholder") == "your-friend@example.com"

    # She shares her list.
    # The page updates to say that it's shared with Oniciferous
    list_page.share_list_with(oni.email)

    # Oniciferous now logs in and goes to his "My lists" page
    force_login(oni)
    my_lists_page.go_to_my_lists_page()

    # He sees Edith's list in there!
    browser.find_element_by_link_text("Get help").click()

    # On the list page, Oniciferous can see that it's Edith's list
    wait_for(lambda: list_page.list_owner == "edith@example.com")

    # He adds a list item
    list_page.add_list_item("Hi Edith!")

    # Edith logs back in and can see Oniciferous's addition
    force_login(edith, target_url=list_url)
    list_page.wait_for_row_in_table("Hi Edith!", 2)
