from django import forms
from django.core.exceptions import ValidationError

from users.models import User

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


class ShareListForm(PlaceholdersMixin, forms.Form):
    sharee = forms.CharField()

    class Meta:
        placeholders = {"sharee": "your-friend@example.com"}

    def __init__(self, *args, list_id=None, sharer=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._list_id = list_id
        self._sharer = sharer

    def save(self):
        return List.objects.share_list(sharee=self.cleaned_data["sharee"], list_id=self._list_id)

    @property
    def list(self):
        return List.objects.get(pk=self._list_id)

    def clean_sharee(self):
        if not User.objects.exists_with_email(self.cleaned_data["sharee"]):
            raise ValidationError("This user doesn't have an account.", code="no_account")
        elif self.cleaned_data["sharee"] == self._sharer.email:
            raise ValidationError("You already own this list.", code="sharer_owns_list")
        return self.cleaned_data["sharee"]
