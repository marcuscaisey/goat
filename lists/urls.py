from django.urls import path

from . import views

app_name = "lists"
urlpatterns = [
    path("new/", views.new_list, name="new-list"),
    path("<int:pk>/", views.view_list, name="view-list"),
    path("users/<str:email>/", views.my_lists, name="my-lists"),
]
