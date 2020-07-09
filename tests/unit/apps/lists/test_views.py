import pytest

from lists.models import Item, List


class TestListView:
    @pytest.mark.django_db
    def test_uses_list_template(self, client, assert_template_used):
        list_ = List.objects.create()
        response = client.get(f"/lists/{list_.pk}/")
        assert_template_used(response, "lists/list.html")

    @pytest.mark.django_db
    def test_displays_only_items_for_that_list(self, client):
        correct_list = List.objects.create()
        Item.objects.create(text="item 1", list=correct_list)
        Item.objects.create(text="item 2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="other item 1", list=other_list)
        Item.objects.create(text="other item 2", list=other_list)

        response = client.get(f"/lists/{correct_list.pk}/")

        assert b"item 1" in response.content
        assert b"item 2" in response.content
        assert b"other item 1" not in response.content
        assert b"other item 2" not in response.content

    @pytest.mark.django_db
    def test_passes_list_to_template(self, client):
        list_ = List.objects.create()
        response = client.get(f"/lists/{list_.pk}/")
        assert response.context["list"] == list_

    @pytest.mark.django_db
    def test_can_save_a_POST_request_to_an_existing_list(self, client):
        list_ = List.objects.create()

        client.post(f"/lists/{list_.pk}/", {"item_text": "A new list item"})

        saved_items = Item.objects
        assert saved_items.count() == 1

        saved_item = saved_items.first()
        assert saved_item.text == "A new list item"
        assert saved_item.list == list_

    @pytest.mark.django_db
    def test_redirects_to_list_view(self, client, assert_redirects):
        list_ = List.objects.create()

        response = client.post(f"/lists/{list_.pk}/", {"item_text": "A new list item"})

        assert_redirects(response, f"/lists/{list_.pk}/")


class TestHome:
    @pytest.mark.django_db
    def test_uses_home_template(self, client, assert_template_used):
        response = client.get("/")
        assert_template_used(response, "lists/home.html")

    @pytest.mark.django_db
    def test_GET_doesnt_save_item(self, client):
        client.get("/")
        assert Item.objects.count() == 0


class TestNewListView:
    @pytest.mark.django_db
    def test_can_save_POST_request(self, client):
        client.post("/lists/new/", data={"item_text": "A new list item"})

        items = Item.objects.all()
        assert items.count() == 1
        assert items.first().text == "A new list item"

    @pytest.mark.django_db
    def test_redirects_after_POST(self, client, assert_redirects):
        response = client.post("/lists/new/", data={"item_text": "A new list item"})
        list_ = List.objects.first()
        assert_redirects(response, f"/lists/{list_.pk}/")

    @pytest.mark.django_db
    def test_validation_errors_are_sent_back_to_home_page_template(self, client, assert_template_used):
        response = client.post("/lists/new/", data={"item_text": ""})
        assert response.status_code == 200
        assert_template_used(response, "lists/home.html")
        assert response.context["error"] == "You can't have an empty list item"

    @pytest.mark.django_db
    def test_empty_list_items_arent_saved(self, client):
        client.post("/lists/new/", data={"item_text": ""})
        assert Item.objects.count() == 0
        assert List.objects.count() == 0
