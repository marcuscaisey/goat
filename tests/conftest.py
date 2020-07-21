import string

import pytest
import pytest_factoryboy

from .factories import ItemFactory, ListFactory, UserFactory

pytest_factoryboy.register(ListFactory)
pytest_factoryboy.register(ItemFactory)
pytest_factoryboy.register(UserFactory)


def pytest_addoption(parser):
    parser.addoption("--functional", action="store_true", help="run functional tests as well")
    parser.addoption("--functional-only", action="store_true", help="run only the functional tests")


def pytest_collection_modifyitems(config, items):
    """
    Run the functional tests with the --functional or --functional-only options.
    """
    functional = config.getoption("--functional")
    functional_only = config.getoption("--functional-only")

    skip_functional_tests = not functional and not functional_only
    skip_unit_tests = functional_only

    functional_skip_marker = pytest.mark.skip(reason="need --functional or --functional-only option to run")
    unit_skip_marker = pytest.mark.skip(reason="--functional-only option set")

    for item in items:
        filename, *_ = item.nodeid.split("::")
        if "functional" in filename and skip_functional_tests:
            item.add_marker(functional_skip_marker)
        elif "functional" not in filename and skip_unit_tests:
            item.add_marker(unit_skip_marker)


@pytest.fixture
def home_url():
    """URL of the home page."""
    return "/"


@pytest.fixture
def login_url():
    """URL of the login page."""
    return "/login/"


@pytest.fixture
def valid_email():
    """A valid email."""
    return "test@email.com"


@pytest.fixture
def valid_password():
    """A valid password."""
    return "password123"


@pytest.fixture
def invalid_email():
    """An invalid email."""
    return "invalidemail"


@pytest.fixture
def long_email():
    """An email that's too long."""
    max_length = 254
    domain_part = "@email.com"
    user_part = (max_length + 1 - len(domain_part)) * "a"
    return f"{user_part}{domain_part}"


@pytest.fixture
def duplicate_email(user):
    """Return an email which a user is already using."""
    return user.email


@pytest.fixture
def short_password(settings):
    """A password that's too short."""
    return string.ascii_letters[: settings.MIN_PASSWORD_LENGTH - 1]


@pytest.fixture
def numeric_password(settings):
    """A password that's entirely numeric."""
    return "1" * settings.MIN_PASSWORD_LENGTH
