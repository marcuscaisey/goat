from django import forms

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
    class Meta:
        model = Item
        fields = ("text",)
        placeholders = {"text": "Enter a to-do item"}
        widgets = {"text": forms.TextInput}
        error_messages = {"text": {"required": "You can't save an empty list item"}}

    def save(self, commit=True, list_=None):
        instance = super().save(commit=False)
        if list_ is None:
            list_ = List.objects.create()
        instance.list = list_

        if commit:
            instance.save()

        return instance
