from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import AuthenticationForm, UserCreationForm


class LoginView(auth_views.LoginView):
    template_name = "users/login.html"
    authentication_form = AuthenticationForm


class LogoutView(auth_views.LogoutView):
    pass


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("users:login")
