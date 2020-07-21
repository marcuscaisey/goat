import pytest
from django.core.exceptions import NON_FIELD_ERRORS
from pytest import lazy_fixture

from users.forms import AuthenticationForm, UserCreationForm
from users.models import User


class TestAuthenticationForm:
    @pytest.mark.django_db
    def test_incorrect_login_error_message(self):
        form = AuthenticationForm(data={"username": "foo", "password": "password"})
        error = "The email address and password provided do not match any of our records."
        assert form.errors[NON_FIELD_ERRORS] == [error]


class TestUserCreationForm:
    @pytest.mark.django_db
    def test_save_creates_valid_user(self, valid_email, valid_password):
        form = UserCreationForm({"email": valid_email, "password1": valid_password, "password2": valid_password})
        form.save()

        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.email == valid_email
        assert user.check_password(valid_password)

    @pytest.mark.parametrize(
        "email,error",
        [
            (lazy_fixture("invalid_email"), "This email address is invalid."),
            (
                lazy_fixture("long_email"),
                "This email address is too long. It must contain no more than 254 characters.",
            ),
            (lazy_fixture("duplicate_email"), "A user with this email address already exists."),
        ],
    )
    @pytest.mark.django_db
    def test_email_validation_errors(self, email, error, valid_password):
        form = UserCreationForm({"email": email, "password1": valid_password, "password2": valid_password})
        assert form.errors["email"] == [error]

    @pytest.mark.parametrize(
        "password,error",
        [
            (lazy_fixture("short_password"), "This password is too short. It must contain at least 10 characters."),
            (lazy_fixture("numeric_password"), "This password is entirely numeric."),
        ],
    )
    @pytest.mark.django_db
    def test_password_validation_errors(self, password, error, valid_email):
        form = UserCreationForm({"email": valid_email, "password1": password, "password2": password})
        assert form.errors["password2"] == [error]

    @pytest.mark.django_db
    def test_validation_error_for_mismatched_passwords(self, valid_email, valid_password):
        form = UserCreationForm({"email": valid_email, "password1": valid_password, "password2": f"{valid_password}1"})
        assert form.errors["password2"] == ["This password doesn't match the one entered before."]
