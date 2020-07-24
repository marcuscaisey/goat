from django.db import models
from django.shortcuts import reverse

from users.models import User


class List(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="lists")

    def get_absolute_url(self):
        return reverse("lists:view-list", args=(self.pk,))

    @property
    def name(self):
        return self.items.first().text


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None, related_name="items")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["text", "list"], name="unique_text_list")]
