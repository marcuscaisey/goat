from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .models import Item, List


def view_list(request, pk):
    error = None
    list_ = List.objects.get(pk=pk)

    if request.method == "POST":
        item = Item(text=request.POST["item_text"], list=list_)
        try:
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, "lists/list.html", {"list": list_, "error": error})


def home_page(request):
    return render(request, "lists/home.html")


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST["item_text"], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        return render(request, "lists/home.html", {"error": "You can't have an empty list item"})
    return redirect(list_)
