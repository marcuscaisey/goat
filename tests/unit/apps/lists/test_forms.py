import pytest
from django import forms
from django.db import models

from lists.forms import ItemForm, PlaceholdersMixin
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

    @pytest.mark.django_db
    def test_validation_error_for_duplicate_list_item(self, item):
        form = ItemForm({"text": item.text}, list_=item.list)

        assert not form.is_valid()
        assert form.errors["text"] == ["You can't save a duplicate item"]


def test_placeholders_mixin():
    class Foo(models.Model):
        bar = models.IntegerField()

        class Meta:
            app_label = "foo"

    class FooForm(PlaceholdersMixin, forms.ModelForm):
        class Meta:
            model = Foo
            fields = ("bar",)
            placeholders = {"bar": "I am the placeholder for bar!"}

    form = FooForm()
    assert 'placeholder="I am the placeholder for bar!"' in str(form["bar"])
