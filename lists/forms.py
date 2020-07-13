from django import forms

from .models import Item, List


class ItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs["placeholder"] = "Enter a to-do item"

    class Meta:
        model = Item
        fields = ("text",)
        error_messages = {"text": {"required": "You can't save an empty list item"}}
        widgets = {"text": forms.TextInput}

    def save(self, commit=True, list_=None):
        instance = super().save(commit=False)
        if list_ is None:
            list_ = List.objects.create()
        instance.list = list_

        if commit:
            instance.save()

        return instance
