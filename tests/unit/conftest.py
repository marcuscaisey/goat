import pytest
from pytest_django.asserts import assertRedirects, assertTemplateUsed


@pytest.fixture
def assert_template_used():
    """Assert that a response used a specific template."""

    def assert_template_used(response, template):
        return assertTemplateUsed(response, template)

    return assert_template_used


@pytest.fixture
def assert_redirects():
    """Assert that a response redirects to a specific url."""

    def assert_redirects(response, url):
        return assertRedirects(response, url)

    return assert_redirects
