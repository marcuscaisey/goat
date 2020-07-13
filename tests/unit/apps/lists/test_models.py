import pytest
from django.core.exceptions import ValidationError

from lists.models import Item, List


class TestItem:
    @pytest.mark.django_db
    def test_saving_and_retrieving(self):
        list_ = List.objects.create()
        Item.objects.create(text="The first (ever) list item", list=list_)

        saved_item = Item.objects.first()

        assert saved_item.text == "The first (ever) list item"
        assert saved_item.list == list_

    @pytest.mark.django_db
    def test_text_cannot_be_empty(self):
        with pytest.raises(ValidationError):
            Item(text="", list=List.objects.create()).full_clean()

    @pytest.mark.django_db
    def test_text_and_list_must_be_unique_together(self):
        list_ = List.objects.create()
        Item.objects.create(text="item text", list=list_)
        with pytest.raises(ValidationError):
            Item(text="item text", list=list_).full_clean()


class TestList:
    @pytest.mark.django_db
    def test_get_absolute_url(self):
        list_ = List.objects.create()
        assert list_.get_absolute_url() == f"/lists/{list_.pk}/"
