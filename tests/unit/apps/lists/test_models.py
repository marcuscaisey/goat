import pytest

from lists.models import Item, List


class TestItem:
    @pytest.mark.django_db
    def test_saving_and_retrieving(self):
        list_ = List.objects.create()
        Item.objects.create(text="The first (ever) list item", list=list_)

        saved_item = Item.objects.first()

        assert saved_item.text == "The first (ever) list item"
        assert saved_item.list == list_
