from django.db import models
from django.shortcuts import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse("lists:view-list", args=(self.pk,))


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)
