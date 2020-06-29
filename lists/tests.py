import pytest
from pytest_django.asserts import assertTemplateUsed

from .models import Item


def assert_template_used(response, template):
    """Assert that a response used a specific template."""
    assertTemplateUsed(response, template)


class TestListView:
    @pytest.mark.django_db
    def test_displays_all_items(self, client):
        Item.objects.create(text="item 1")
        Item.objects.create(text="item 2")

        response = client.get("/lists/the-only-list-in-the-world/")

        assert b"item 1" in response.content
        assert b"item 2" in response.content

    @pytest.mark.django_db
    def test_uses_list_template(self, client):
        response = client.get("/lists/the-only-list-in-the-world/")
        assert_template_used(response, "lists/list.html")


class TestHome:
    @pytest.mark.django_db
    def test_uses_home_template(self, client):
        response = client.get("/")
        assert_template_used(response, "lists/home.html")

    @pytest.mark.django_db
    def test_GET_doesnt_save_item(self, client):
        client.get("/")
        assert Item.objects.count() == 0

    @pytest.mark.django_db
    def test_can_save_POST_request(self, client):
        client.post("/", data={"item_text": "A new list item"})

        items = Item.objects.all()
        assert items.count() == 1
        assert items.first().text == "A new list item"

    @pytest.mark.django_db
    def test_redirects_after_POST(self, client):
        response = client.post("/", data={"item_text": "A new list item"})

        assert response.status_code == 302
        assert response.url == "/lists/the-only-list-in-the-world/"
