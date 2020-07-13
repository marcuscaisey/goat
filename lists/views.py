from django.shortcuts import redirect, render

from .forms import ItemForm
from .models import List


def view_list(request, pk):
    list_ = List.objects.get(pk=pk)

    if request.method == "POST":
        form = ItemForm(request.POST, list_=list_)
        if form.is_valid():
            form.save()
            return redirect(list_)
    else:
        form = ItemForm()

    return render(request, "lists/list.html", {"list": list_, "form": form})


def home_page(request):
    return render(request, "lists/home.html", {"form": ItemForm()})


def new_list(request):
    form = ItemForm(request.POST)
    if form.is_valid():
        item = form.save()
        return redirect(item.list)
    else:
        return render(request, "lists/home.html", {"form": form})
