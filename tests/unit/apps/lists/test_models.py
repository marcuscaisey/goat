import pytest
from django.core.exceptions import ValidationError

from lists.models import Item


class TestItem:
    @pytest.mark.django_db
    def test_saving_and_retrieving(self, list):
        Item.objects.create(text="The first (ever) list item", list=list)

        saved_item = Item.objects.first()

        assert saved_item.text == "The first (ever) list item"
        assert saved_item.list == list

    @pytest.mark.django_db
    def test_text_cannot_be_empty(self, item_factory):
        with pytest.raises(ValidationError):
            item_factory.build(text="").full_clean()

    @pytest.mark.django_db
    def test_text_and_list_must_be_unique_together(self, item, item_factory):
        with pytest.raises(ValidationError):
            item_factory.build(text=item.text, list=item.list).full_clean()


class TestList:
    @pytest.mark.django_db
    def test_get_absolute_url(self, list):
        assert list.get_absolute_url() == f"/lists/{list.pk}/"
