import time

import pytest
import seleniumlogin
from selenium import webdriver
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote import webelement


@pytest.fixture
def to_do_table_id():
    return "to-do_items"


@pytest.fixture
def row_in_todo_table(browser, to_do_table_id):
    """
    A function which returns if a row with the given text is in the to-do list
    table.
    """

    def row_in_todo_table(text):
        table = browser.find_element_by_id(to_do_table_id)
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
def field(browser):
    """A function which returns a form field."""

    def field(name) -> webelement.WebElement:
        return browser.find_element_by_id(f"id_{name}")

    return field


@pytest.fixture
def field_error(browser):
    """A function which returns the error for a form field."""

    def field_error(name) -> webelement.WebElement:
        return browser.find_element_by_id(f"id_{name}-error")

    return field_error


@pytest.fixture
def new_item_input_id():
    """ID of the new item input."""
    return "id_text"


@pytest.fixture
def new_item_input(browser, new_item_input_id):
    """A function which gets the new item input from the page."""

    def new_item_input():
        return browser.find_element_by_id(new_item_input_id)

    return new_item_input


@pytest.fixture
def force_login(browser, base_url):
    """
    Function which logs in a user to the current selenium browser session.

    Args:
        user (User): The user to log in.
    """

    def force_login(user):
        seleniumlogin.force_login(user, browser, base_url)

    return force_login


@pytest.fixture
def browser(selenium: webdriver.Firefox) -> webdriver.Firefox:
    return selenium


@pytest.fixture
def add_list_item(browser, wait_for, row_in_todo_table, field, to_do_table_id):
    """Add an item to the list on the current page."""

    def add_list_item(text):
        rows = len(browser.find_elements_by_css_selector(f"#{to_do_table_id} tr"))
        field("text").send_keys(text, Keys.ENTER)
        wait_for(row_in_todo_table, f"{rows + 1}: {text}")

    return add_list_item
