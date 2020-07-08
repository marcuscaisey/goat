import os
import time

import pytest
from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions


@pytest.fixture
def browser_factory():
    """A factory which returns new firefox browsers to use during tests."""
    browsers = []

    def browser_factory():
        browser = webdriver.Firefox()
        browsers.append(browser)
        return browser

    yield browser_factory

    for browser in browsers:
        browser.quit()


@pytest.fixture
def browser(browser_factory):
    """A new browser instance."""
    return browser_factory()


@pytest.fixture(scope="session")
def live_server_url(live_server):
    return os.getenv("STAGING_SERVER", live_server.url)


MAX_WAIT = 10


@pytest.fixture
def wait_for_row_in_todo_table():
    """
    A function which checks if a row with the given text is in the to-do list
    table.
    """

    def wait_for_row_in_todo_table(text, browser):
        start = time.time()
        while True:
            try:
                table = browser.find_element_by_id("to-do_items")
                rows = table.find_elements_by_tag_name("tr")
                assert text in [row.text for row in rows]
                return
            except (AssertionError, selenium_exceptions.WebDriverException):
                if time.time() - start > MAX_WAIT:
                    raise
                time.sleep(0.5)

    return wait_for_row_in_todo_table
