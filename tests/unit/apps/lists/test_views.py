import pytest

from lists.forms import ItemForm
from lists.models import Item, List


@pytest.fixture
def view_list_url_factory():
    """Function which returns the view list page url for a list."""

    def view_list_url_factory(list):
        return f"/lists/{list.pk}/"

    return view_list_url_factory


class TestViewList:
    @pytest.fixture
    def view_list_url(self, list, view_list_url_factory):
        """URL of the view list page for a list."""
        return view_list_url_factory(list)

    @pytest.fixture
    def list_template(self):
        """Template that the view list page uses."""
        return "lists/list.html"

    @pytest.fixture
    def get_response(self, client, view_list_url):
        """Response to a GET request to the view list page for a list."""
        return client.get(view_list_url)

    @pytest.mark.django_db
    def test_uses_list_template(self, get_response, assert_template_used, list_template):
        assert_template_used(get_response, list_template)

    @pytest.mark.django_db
    def test_passes_item_form_to_template(self, get_response):
        assert isinstance(get_response.context["form"], ItemForm)

    @pytest.mark.django_db
    def test_passes_list_to_template(self, get_response, list):
        assert get_response.context["list"] == list

    @pytest.fixture
    def success_response(self, client, view_list_url):
        """Response to a successful POST request to the view list page."""
        return client.post(view_list_url, {"text": "A new list item"})

    @pytest.mark.django_db
    def test_can_save_a_POST_request_to_an_existing_list(self, success_response, list):
        saved_items = Item.objects
        assert saved_items.count() == 1

        saved_item = saved_items.first()
        assert saved_item.text == "A new list item"
        assert saved_item.list == list

    @pytest.mark.django_db
    def test_redirects_to_list_view(self, success_response, view_list_url, assert_redirects):
        assert_redirects(success_response, view_list_url)

    @pytest.fixture
    def empty_input_response(self, client, view_list_url):
        """
        Response to a POST request to the view list page with invalid input.
        """
        return client.post(view_list_url, data={"text": ""})

    @pytest.mark.django_db
    def test_empty_input_renders_list_template(self, empty_input_response, assert_template_used, list_template):
        assert empty_input_response.status_code == 200
        assert_template_used(empty_input_response, list_template)

    @pytest.mark.django_db
    def test_empty_input_passes_list_to_template(self, empty_input_response, list):
        assert empty_input_response.context["list"] == list

    @pytest.mark.django_db
    def test_empty_input_passes_form_to_template(self, empty_input_response, assert_form_is_instance_with_errors):
        assert_form_is_instance_with_errors(empty_input_response.context["form"], ItemForm)

    @pytest.mark.django_db
    def test_empty_list_items_arent_saved(self, empty_input_response):
        assert Item.objects.count() == 0

    @pytest.fixture
    def duplicate_item_response(self, client, view_list_url_factory, item):
        """
        Response to a POST request to the view list page with duplicate text
        input.
        """
        return client.post(view_list_url_factory(item.list), data={"text": item.text})

    @pytest.mark.django_db
    def test_duplicate_list_item_renders_list_template(self, duplicate_item_response, assert_template_used):
        assert duplicate_item_response.status_code == 200
        assert_template_used(duplicate_item_response, "lists/list.html")

    @pytest.mark.django_db
    def test_duplicate_list_item_passes_list_to_template(self, duplicate_item_response, list):
        assert duplicate_item_response.context["list"] == list

    @pytest.mark.django_db
    def test_duplicate_list_item_passes_form_to_template(
        self, duplicate_item_response, assert_form_is_instance_with_errors
    ):
        assert_form_is_instance_with_errors(duplicate_item_response.context["form"], ItemForm)

    @pytest.mark.django_db
    def test_duplicate_list_items_arent_saved(self, duplicate_item_response):
        assert Item.objects.count() == 1


@pytest.fixture
def home_template():
    """Template that the home page uses."""
    return "lists/home.html"


class TestHome:
    @pytest.fixture
    def get_response(self, client, home_url):
        """Response to a GET request for the home page."""
        return client.get(home_url)

    @pytest.mark.django_db
    def test_uses_home_template(self, get_response, assert_template_used, home_template):
        assert_template_used(get_response, home_template)

    @pytest.mark.django_db
    def test_uses_item_form(self, get_response):
        assert isinstance(get_response.context["form"], ItemForm)

    @pytest.mark.django_db
    def test_GET_doesnt_save_item(self, get_response):
        assert Item.objects.count() == 0


class TestNewList:
    @pytest.fixture
    def new_list_url(self):
        """URL of the new list view."""
        return "/lists/new/"

    @pytest.fixture
    def success_response(self, new_list_url, client):
        """Response to a successful POST request to the new list view."""
        return client.post(new_list_url, data={"text": "A new list item"})

    @pytest.mark.django_db
    def test_can_save_POST_request(self, success_response):
        items = Item.objects.all()
        assert items.count() == 1
        assert items.first().text == "A new list item"

    @pytest.mark.django_db
    def test_redirects_after_POST(self, success_response, assert_redirects, view_list_url_factory):
        list_ = List.objects.first()
        assert_redirects(success_response, view_list_url_factory(list_))

    @pytest.fixture
    def empty_input_response(self, client, new_list_url):
        """Response to a POST request to the new list view with empty text input."""
        return client.post(new_list_url, data={"text": ""})

    @pytest.mark.django_db
    def test_empty_input_renders_home_template(self, empty_input_response, assert_template_used, home_template):
        assert empty_input_response.status_code == 200
        assert_template_used(empty_input_response, home_template)

    @pytest.mark.django_db
    def test_empty_input_passes_form_to_template(self, empty_input_response, assert_form_is_instance_with_errors):
        assert_form_is_instance_with_errors(empty_input_response.context["form"], ItemForm)

    @pytest.mark.django_db
    def test_empty_list_items_arent_saved(self, empty_input_response):
        assert Item.objects.count() == 0
        assert List.objects.count() == 0
