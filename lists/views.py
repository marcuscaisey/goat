from django.shortcuts import redirect, render

from .models import Item, List


def view_list(request):
    items = Item.objects.all()
    return render(request, "lists/list.html", {"items": items})


def home_page(request):
    return render(request, "lists/home.html")


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect("/lists/the-only-list-in-the-world/")
