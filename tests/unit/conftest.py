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


@pytest.fixture
def assert_form_is_instance_with_errors():
    """
    Assert that a form is an instance of a specified type and that it has
    errors.
    """

    def assert_form_is_instance_with_errors(form, type_):
        assert isinstance(form, type_)
        assert form.errors

    return assert_form_is_instance_with_errors


@pytest.fixture
def home_url():
    """URL of the home page."""
    return "/"
