import os
import time

import pytest
from selenium.common import exceptions as selenium_exceptions


@pytest.fixture(scope="session")
def live_server_url(live_server):
    return os.getenv("STAGING_SERVER", live_server.url)


@pytest.fixture
def wait_for_row_in_todo_table(wait_for):
    """
    A function which checks if a row with the given text is in the to-do list
    table.
    """

    def wait_for_row_in_todo_table(text, browser):
        def row_in_todo_table():
            table = browser.find_element_by_id("to-do_items")
            rows = table.find_elements_by_tag_name("tr")
            return text in [row.text for row in rows]

        return wait_for(row_in_todo_table)

    return wait_for_row_in_todo_table


@pytest.fixture
def wait_for():
    """
    Assert on the result of a callable. If an AssertionError or
    WebDriverException is raised, keep retrying the callable. Once a period of
    time has passed, allow the exception to be raised.

    Args:
        f (callable): A callable to assert on.
        timeout (float): The number of seconds until the callable should stop
            being retried. Defaults to 10.
        wait_time (float): The number of seconds to wait between retries of the
            callable. Defaults to 0.5.

    Raises:
        AssertionError: If timeout seconds have passed and the callable returns
            False.
        WebDriverException: If timeout seconds have passed and the callable
            raises a WebDriverException.
    """

    def wait_for(f, timeout=10, wait_time=0.5):
        start = time.time()
        while True:
            try:
                assert f()
                return
            except (AssertionError, selenium_exceptions.WebDriverException):
                if time.time() - start > timeout:
                    raise
                time.sleep(wait_time)

    return wait_for


@pytest.fixture
def get_item_input():
    """A function which gets the item input element from the page."""

    def get_item_input(browser):
        return browser.find_element_by_id("id_text")

    return get_item_input
