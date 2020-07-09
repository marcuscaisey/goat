from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .models import Item, List


def view_list(request, pk):
    if request.method == "POST":
        list_ = List.objects.get(pk=pk)
        Item.objects.create(text=request.POST["item_text"], list=list_)
        return redirect(f"/lists/{list_.pk}/")

    return render(request, "lists/list.html", {"list": List.objects.get(pk=pk)})


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
    return redirect(f"/lists/{list_.pk}/")
