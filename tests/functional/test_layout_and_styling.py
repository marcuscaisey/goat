import pytest


def test_layout(browser, home_url, new_item_input):
    browser.set_window_size(1024, 768)

    browser.get(home_url)

    input_ = new_item_input()
    assert input_.location["x"] + input_.size["width"] / 2 == pytest.approx(512, abs=10)
