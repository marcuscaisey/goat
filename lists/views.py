from django.shortcuts import redirect, render

from .models import Item, List


def view_list(request, pk):
    return render(request, "lists/list.html", {"list": List.objects.get(pk=pk)})


def home_page(request):
    return render(request, "lists/home.html")


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/lists/{list_.pk}/")


def add_item(request, pk):
    list_ = List.objects.get(pk=pk)
    Item.objects.create(text=request.POST["item_text"], list=list_)
    return redirect(f"/lists/{list_.pk}/")
