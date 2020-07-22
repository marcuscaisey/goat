import pytest


class TestList:
    @pytest.mark.django_db
    def test_get_absolute_url(self, list):
        assert list.get_absolute_url() == f"/lists/{list.pk}/"
