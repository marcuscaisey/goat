from django.db import models
from django.shortcuts import reverse

from users.models import User


class List(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="lists")

    def get_absolute_url(self):
        return reverse("lists:view-list", args=(self.pk,))

    @staticmethod
    def create_new(first_item_text, owner=None):
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_

    @property
    def name(self):
        return self.items.first().text


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None, related_name="items")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["text", "list"], name="unique_text_list")]
