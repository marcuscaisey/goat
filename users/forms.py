from django.contrib.auth import forms as auth_forms

from .models import User


class AuthenticationForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages["invalid_login"] = "The %(username)s and password provided do not match any of our records."


class UserCreationForm(auth_forms.UserCreationForm):
    error_messages = {"password_mismatch": "This password doesn't match the one entered before."}

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        error_messages = {
            "email": {
                "invalid": "This email address is invalid.",
                "max_length": (
                    "This email address is too long. It must contain no more than %(limit_value)s characters."
                ),
                "unique": "A user with this email address already exists.",
            },
        }
