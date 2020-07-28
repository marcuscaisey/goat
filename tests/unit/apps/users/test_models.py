import pytest

from users.models import User


@pytest.mark.django_db
class TestUserManager:
    def test_exists_with_email_is_True_if_user_exists(self, user):
        assert User.objects.exists_with_email(user.email)

    def test_exists_with_email_is_False_if_user_doesnt_exist(self):
        assert not User.objects.exists_with_email("john.smith@gmail.com")


class TestUser:
    @pytest.mark.django_db
    def test_can_save_more_than_one_user(self, user_factory):
        user_factory()
        user_factory()
