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
    def test_saves_item_to_list(self, list):
        form = ItemForm({"text": "New item text"}, list_=list)
        form.save()

        assert Item.objects.count() == 1
        assert List.objects.count() == 1

        saved_item = Item.objects.first()
        assert saved_item.text == "New item text"
        assert saved_item.list == list

    def test_validation_error_for_blank_item(self):
        form = ItemForm({"text": ""})

        assert not form.is_valid()
        assert form.errors["text"] == ["You can't save an empty list item"]

    @pytest.mark.django_db
    def test_validation_error_for_blank_item_with_existing_list(self, list):
        form = ItemForm({"text": ""}, list_=list)

        assert not form.is_valid()
        assert form.errors["text"] == ["You can't save an empty list item"]

    def test_text_field_has_placeholder(self):
        form = ItemForm()
        assert form.fields["text"].widget.attrs["placeholder"] == "Enter a to-do item"

    def test_text_field_is_TextInput(self):
        form = ItemForm()
        assert isinstance(form.fields["text"].widget, forms.TextInput)

    @pytest.mark.django_db
    def test_validation_error_for_duplicate_list_item(self, list):
        Item.objects.create(text="item text", list=list)
        form = ItemForm({"text": "item text"}, list_=list)

        assert not form.is_valid()
        assert form.errors["text"] == ["You can't save a duplicate item"]
