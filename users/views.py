from django.contrib.auth import views as auth_views

from .forms import AuthenticationForm


class LoginView(auth_views.LoginView):
    template_name = "users/login.html"
    authentication_form = AuthenticationForm


class LogoutView(auth_views.LogoutView):
    pass
