import pytest
from django import forms
from django.db import models

from lists.forms import ItemForm, NewListForm, PlaceholdersMixin
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


class TestNewListForm:
    @pytest.fixture
    def mock_List_create_new(self, mocker):
        """A mock List.create_new."""
        return mocker.patch("lists.forms.List.create_new")

    @pytest.fixture
    def mock_user(self, mocker):
        """A mock User instance."""
        return mocker.Mock()

    def test_save_creates_new_list_if_user_not_authenticated(self, mock_List_create_new, mock_user):
        mock_user.is_authenticated = False
        form = NewListForm(data={"text": "new item text"})
        form.is_valid()

        form.save(owner=mock_user)

        mock_List_create_new.assert_called_once_with(first_item_text="new item text")

    def test_save_creates_new_list_with_owner_if_user_authenticated(self, mock_user, mock_List_create_new):
        mock_user.is_authenticated = True
        form = NewListForm(data={"text": "new item text"})
        form.is_valid()

        form.save(owner=mock_user)

        mock_List_create_new.assert_called_once_with(first_item_text="new item text", owner=mock_user)

    def test_save_returns_new_list_object(self, mock_user, mock_List_create_new):
        form = NewListForm(data={"text": "new item text"})
        form.is_valid()

        list_ = form.save(owner=mock_user)

        assert list_ == mock_List_create_new.return_value
