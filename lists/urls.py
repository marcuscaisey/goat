from django.urls import path

from . import views

app_name = "lists"
urlpatterns = [
    path("", views.home_page, name="home"),
    path("lists/new/", views.new_list, name="new-list"),
    path("lists/<int:pk>/add_item/", views.add_item, name="add-item"),
    path("lists/<int:pk>/", views.view_list, name="view-list"),
]
