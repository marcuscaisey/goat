import pytest
from django import forms

from lists.forms import ItemForm
from lists.models import Item, List


class TestItemForm:
    @pytest.mark.django_db
    def test_saves_item_and_creates_list(self):
        form = ItemForm({"text": "New item text"})
        form.save()

        assert Item.objects.count() == 1
        assert List.objects.count() == 1

        saved_item = Item.objects.first()
        assert saved_item.text == "New item text"
        assert saved_item.list is not None

    @pytest.mark.django_db
    def test_saves_item_to_list(self):
        list_ = List.objects.create()
        form = ItemForm({"text": "New item text"})
        form.save(list_=list_)

        assert Item.objects.count() == 1
        assert List.objects.count() == 1

        saved_item = Item.objects.first()
        assert saved_item.text == "New item text"
        assert saved_item.list == list_

    def test_validation_error_for_blank_item(self):
        form = ItemForm({"text": ""})

        assert not form.is_valid()
        assert "text" in form.errors

    def test_text_field_has_placeholder(self):
        form = ItemForm()
        assert "placeholder" in form.fields["text"].widget.attrs

    def test_text_field_is_TextInput(self):
        form = ItemForm()
        assert isinstance(form.fields["text"].widget, forms.TextInput)
