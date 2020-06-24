from django.urls import resolve

from .views import home_page


def test_root_url_resolves_to_home_page_view():
    match = resolve("/")
    assert match.func == home_page
