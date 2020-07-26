from django import forms
from django.core.exceptions import ValidationError

from .models import Item, List


class PlaceholdersMixin:
    """
    Sets the placeholders on a Form's widgets. Add a "placeholders" dict to the
    Meta options, which maps field names to placeholder texts.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = getattr(self.Meta, "placeholders", {})
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs["placeholder"] = placeholder


class ItemForm(PlaceholdersMixin, forms.ModelForm):
    def __init__(self, *args, list_=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = list_

    class Meta:
        model = Item
        fields = ("text",)
        placeholders = {"text": "Enter a to-do item"}
        widgets = {"text": forms.TextInput}
        error_messages = {
            "text": {"required": "You can't save an empty list item", "unique": "You can't save a duplicate item"}
        }

    def save(self, commit=True):
        """
        Create a list if the internal instance doesn't already have one set.
        """
        if self.instance.list_id is None:
            self.instance.list = List.objects.create()
        return super().save(commit=commit)

    def clean_text(self):
        """
        Check for items in the same list with the same list text if the
        internal instance has a list set.
        """
        if (
            self.instance.list_id is None
            or not Item.objects.filter(text=self.cleaned_data["text"], list=self.instance.list).exists()
        ):
            return self.cleaned_data["text"]
        else:
            self._update_errors(ValidationError({"text": ValidationError("Text is not unique", code="unique")}))


class NewListForm(ItemForm):
    def save(self, owner):
        if owner.is_authenticated:
            return List.create_new(first_item_text=self.cleaned_data["text"], owner=owner)
        else:
            return List.create_new(first_item_text=self.cleaned_data["text"])
