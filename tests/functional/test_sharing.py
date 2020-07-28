from selenium.webdriver.common.keys import Keys


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


def test_cant_share_a_list_with_a_user_without_an_account(browser, user, base_url, force_login, list_page, wait_for):
    # Edith logs in and creates a list
    force_login(user, target_url=base_url)
    list_page.add_list_item("Buy milk")

    # She shares her list with her friend John
    list_page.share_box.send_keys("john.smith@gmail.com", Keys.ENTER)

    # An error shows up below the share box saying that John doesn't have an
    # account
    wait_for(lambda: list_page.share_box_error == "This user doesn't have an account.")
    assert "john.smith@gmail.com" not in list_page.shared_with_list


def test_cant_share_a_list_with_the_lists_owner(browser, user, base_url, force_login, list_page, wait_for):
    # Edith logs in and creates a list
    force_login(user, target_url=base_url)
    list_page.add_list_item("Buy milk")

    # She shares the list with her friend, but accidentally types in her own
    # email
    list_page.share_box.send_keys(user.email, Keys.ENTER)

    # An error shows up below the share box saying that she already owns the
    # list
    wait_for(lambda: list_page.share_box_error == "You already own this list.")
    assert user.email not in list_page.shared_with_list
