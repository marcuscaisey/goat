import pytest


def test_layout(selenium, live_server_url, get_item_input):
    selenium.set_window_size(1024, 768)

    selenium.get(live_server_url)

    input_ = get_item_input(selenium)
    assert input_.location["x"] + input_.size["width"] / 2 == pytest.approx(512, abs=10)
