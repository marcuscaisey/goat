from django.shortcuts import redirect, render

from users.models import User

from .forms import ItemForm, NewListForm
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
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, "lists/home.html", {"form": form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, "lists/my_lists.html", {"owner": owner})
