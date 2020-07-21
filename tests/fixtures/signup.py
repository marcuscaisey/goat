import string

import pytest


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
