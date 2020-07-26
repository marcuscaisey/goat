import pytest

from lists.models import Item, List


@pytest.mark.django_db
class TestList:
    def test_get_absolute_url(self, list):
        assert list.get_absolute_url() == f"/lists/{list.pk}/"

    def test_create_new_creates_list_and_item(self):
        List.create_new(first_item_text="new item text")

        saved_item = Item.objects.first()
        saved_list = List.objects.first()
        assert saved_item.text == "new item text"
        assert saved_item.list == saved_list

    def test_create_new_optionally_saves_owner(self, user):
        List.create_new(first_item_text="new item text", owner=user)

        saved_item = Item.objects.first()
        saved_list = List.objects.first()
        assert saved_item.text == "new item text"
        assert saved_item.list == saved_list
        assert saved_list.owner == user

    def test_create_new_returns_new_list_object(self):
        list_ = List.create_new(first_item_text="new item text")
        assert list_ == List.objects.first()

    def test_name_is_first_item_text(self, item):
        assert item.list.name == item.text
