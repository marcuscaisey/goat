import pytest


class TestList:
    @pytest.mark.django_db
    def test_get_absolute_url(self, list):
        assert list.get_absolute_url() == f"/lists/{list.pk}/"

    @pytest.mark.django_db
    def test_name(self, item):
        assert item.list.name == item.text
