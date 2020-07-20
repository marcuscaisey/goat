import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from users.models import User


class TestUser:
    @pytest.fixture
    def user_fields(self):
        """A list of fields on the User model."""
        return [field.name for field in User._meta.fields]

    @pytest.mark.django_db
    def test_saving_and_retrieving(self):
        user = User(email="test@example.org")
        user.set_password("password")
        user.save()

        saved_user = User.objects.first()

        assert saved_user.email == "test@example.org"
        assert user.check_password("password")

    def test_email_is_username(self, user_factory):
        user = user_factory.build(email="test@example.org")

        assert user.get_username() == "test@example.org"

    def test_email_cannot_be_blank(self, user_factory, user_fields):
        user_fields.remove("email")
        with pytest.raises(ValidationError, match="blank"):
            user_factory.build(email="").clean_fields(exclude=user_fields)

    @pytest.mark.django_db
    def test_email_is_unique(self, user, user_factory):
        with pytest.raises(IntegrityError, match="email"):
            user_factory(email=user.email)
