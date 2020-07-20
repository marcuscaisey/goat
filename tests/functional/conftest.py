import time

import pytest
import seleniumlogin
from selenium.common import exceptions as selenium_exceptions


@pytest.fixture(scope="session")
def base_url(live_server, base_url):
    url = base_url if base_url else live_server.url
    if not url.endswith("/"):
        url += "/"
    return url


@pytest.fixture
def row_in_todo_table(selenium):
    """
    A function which returns if a row with the given text is in the to-do list
    table.
    """

    def row_in_todo_table(text):
        table = selenium.find_element_by_id("to-do_items")
        rows = table.find_elements_by_tag_name("tr")
        return text in [row.text for row in rows]

    return row_in_todo_table


@pytest.fixture
def wait_for():
    """
    Assert on the result of a callable, f. If an AssertionError or
    WebDriverException is raised, keep retrying f. Once a period of time has
    passed, allow the exception to be raised.

    Args:
        f (callable): A callable to assert on.
        *args: Positional arguments to call f with.
        timeout (float): The number of seconds until f should stop being
            retried. Defaults to 10.
        wait_time (float): The number of seconds to wait between retries of f.
            Defaults to 0.5.
        **kwargs: Keyword arguments to call f with.

    Raises:
        AssertionError: If timeout seconds have passed and f returns False.
        WebDriverException: If timeout seconds have passed and f raises a
            WebDriverException.
    """

    def wait_for(f, *args, timeout=10, wait_time=0.5, **kwargs):
        start = time.time()
        while True:
            try:
                assert f(*args, **kwargs)
                return
            except (AssertionError, selenium_exceptions.WebDriverException):
                if time.time() - start > timeout:
                    raise
                time.sleep(wait_time)

    return wait_for


@pytest.fixture
def get_item_input(selenium):
    """A function which gets the item input element from the page."""

    def get_item_input():
        return selenium.find_element_by_id("id_text")

    return get_item_input


@pytest.fixture
def force_login(selenium, base_url):
    """
    Function which logs in a user to the current selenium browser session.

    Args:
        user (User): The user to log in.
    """

    def force_login(user):
        seleniumlogin.force_login(user, selenium, base_url)

    return force_login
