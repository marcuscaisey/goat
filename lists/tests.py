from django.http import HttpRequest
from django.urls import resolve

from .views import home_page


def test_root_url_resolves_to_home_page_view():
    match = resolve("/")
    assert match.func == home_page


def test_home_page_returns_correct_html():
    request = HttpRequest()
    response = home_page(request)
    html = response.content.decode("utf8")
    assert html.startswith("<html>")
    assert "<title>To-Do lists</title>" in html
    assert html.endswith("</html>")
