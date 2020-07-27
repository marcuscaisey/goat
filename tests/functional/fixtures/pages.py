import functools
import time

import pytest
from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.common.keys import Keys


@pytest.fixture
def list_page(browser, base_url):
    return ListPage(browser, base_url)


@pytest.fixture
def my_lists_page(browser, base_url):
    return MyListsPage(browser, base_url)


def wait(timeout=10, wait_time=0.5):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            start = time.time()
            while True:
                try:
                    return f(*args, **kwargs)
                except (AssertionError, selenium_exceptions.WebDriverException):
                    if time.time() - start > timeout:
                        raise
                    time.sleep(wait_time)

        return wrapper

    return decorator


@wait()
def _wait_for(f, *args, **kwargs):
    assert f(*args, **kwargs)


class Page:
    def __init__(self, browser: webdriver.Firefox, base_url):
        self.browser = browser
        self.base_url = base_url


class ListPage(Page):
    @property
    def table_rows(self):
        return self.browser.find_elements_by_css_selector("#to-do_items tr")

    @wait()
    def wait_for_row_in_table(self, item_text, item_number):
        expected_row_text = f"{item_number}: {item_text}"
        assert expected_row_text in [row.text for row in self.table_rows]
        return self

    @property
    def new_item_input(self):
        return self.browser.find_element_by_id("id_text")

    def add_list_item(self, item_text):
        rows = len(self.table_rows)
        self.new_item_input.send_keys(item_text, Keys.ENTER)
        self.wait_for_row_in_table(item_text, rows + 1)
        return self

    @property
    def share_box(self):
        return self.browser.find_element_by_css_selector("input[name=sharee]")

    @property
    def shared_with_list(self):
        return self.browser.find_elements_by_css_selector(".list-sharee")

    def share_list_with(self, email):
        self.share_box.send_keys(email, Keys.ENTER)
        _wait_for(lambda: email in [item.text for item in self.shared_with_list])
        return self

    @property
    def list_owner(self):
        return self.browser.find_element_by_id("list-owner").text


class MyListsPage(Page):
    def got_to_my_lists_page(self):
        self.browser.get(self.base_url)
        self.browser.find_element_by_link_text("My lists").click()
        _wait_for(lambda: self.browser.find_element_by_tag_name("h1").text == "My lists")
        return self
