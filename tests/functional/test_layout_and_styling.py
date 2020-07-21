import pytest


def test_layout(selenium, home_url, get_item_input):
    selenium.set_window_size(1024, 768)

    selenium.get(home_url)

    input_ = get_item_input()
    assert input_.location["x"] + input_.size["width"] / 2 == pytest.approx(512, abs=10)
