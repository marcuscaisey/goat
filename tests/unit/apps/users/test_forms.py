import pytest
from django.core.exceptions import NON_FIELD_ERRORS

from users.forms import AuthenticationForm


class TestAuthenticationForm:
    @pytest.mark.django_db
    def test_incorrect_login_error_message(self):
        form = AuthenticationForm(data={"username": "foo", "password": "password"})
        error = "The email address and password provided do not match any of our records."
        assert form.errors[NON_FIELD_ERRORS] == [error]
