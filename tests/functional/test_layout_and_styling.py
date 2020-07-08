import pytest


def test_layout(browser, live_server_url):
    browser.set_window_size(1024, 768)

    browser.get(live_server_url)

    input_ = browser.find_element_by_id("new_item_input")
    assert input_.location["x"] + input_.size["width"] / 2 == pytest.approx(512, abs=10)
