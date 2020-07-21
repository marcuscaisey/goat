import pytest


@pytest.fixture
def home_url():
    """URL of the home page."""
    return "/"


@pytest.fixture
def login_url():
    """URL of the login page."""
    return "/login/"
