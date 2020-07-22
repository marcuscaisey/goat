import pytest


@pytest.fixture(scope="session")
def base_url(live_server, base_url):
    return base_url if base_url else live_server.url


@pytest.fixture
def home_url(base_url, home_url):
    """URL of the home page."""
    return base_url + home_url


@pytest.fixture
def login_url(base_url, login_url):
    """URL of the login page."""
    return base_url + login_url


@pytest.fixture
def signup_url(base_url):
    """URL of the signup page."""
    return base_url + "/signup/"
