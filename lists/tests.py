import pytest
from pytest_django.asserts import assertRedirects, assertTemplateUsed

from .models import Item, List


def assert_template_used(response, template):
    """Assert that a response used a specific template."""
    assertTemplateUsed(response, template)


def assert_redirects(response, url):
    """Assert that a response redirects to a specific url."""
    assertRedirects(response, url)


class TestListView:
    @pytest.mark.django_db
    def test_displays_all_items(self, client):
        list_ = List.objects.create()
        Item.objects.create(text="item 1", list=list_)
        Item.objects.create(text="item 2", list=list_)

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


class TestNewListView:
    @pytest.mark.django_db
    def test_can_save_POST_request(self, client):
        client.post("/lists/new/", data={"item_text": "A new list item"})

        items = Item.objects.all()
        assert items.count() == 1
        assert items.first().text == "A new list item"

    @pytest.mark.django_db
    def test_redirects_after_POST(self, client):
        response = client.post("/lists/new/", data={"item_text": "A new list item"})
        assert_redirects(response, "/lists/the-only-list-in-the-world/")


class ListAndItemModelsTest:
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        first_saved_item, second_saved_item = Item.objects.all()

        assert saved_list == list_
        assert first_saved_item.text == "The first (ever) list item"
        assert first_saved_item.list == list_
        assert second_saved_item.text == "Item the second"
        assert second_saved_item.list == list_
