import pytest


class TestUser:
    @pytest.mark.django_db
    def test_can_save_more_than_one_user(self, user_factory):
        user_factory()
        user_factory()
