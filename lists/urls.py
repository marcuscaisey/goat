from django.urls import path

from . import views

app_name = "lists"
urlpatterns = [
    path("", views.home_page, name="home"),
]
