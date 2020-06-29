from django.urls import path

from . import views

app_name = "lists"
urlpatterns = [
    path("new/", views.new_list, name="new-list"),
    path("<int:pk>/add_item/", views.add_item, name="add-item"),
    path("<int:pk>/", views.view_list, name="view-list"),
]
