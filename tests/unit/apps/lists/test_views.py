import pytest

from lists.forms import ItemForm
from lists.models import Item, List


@pytest.fixture
def view_list_url_factory():
    """Function which returns the view list page url for a list."""

    def view_list_url_factory(list):
        return f"/lists/{list.pk}/"

    return view_list_url_factory


@pytest.fixture
def mock_item_form(mocker):
    """A mock ItemForm."""
    return mocker.patch("lists.views.ItemForm", autospec=True)


@pytest.fixture
def mock_item_form_instance(mock_item_form):
    """A mock ItemForm instance."""
    return mock_item_form.return_value


@pytest.mark.django_db
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

    def test_uses_list_template(self, get_response, assert_template_used, list_template):
        assert get_response.status_code == 200
        assert_template_used(get_response, list_template)

    def test_passes_item_form_to_template(self, get_response):
        assert isinstance(get_response.context["form"], ItemForm)

    def test_passes_list_to_template(self, get_response, list):
        assert get_response.context["list"] == list

    @pytest.fixture
    def success_response(self, client, view_list_url):
        """Response to a successful POST request to the view list page."""
        return client.post(view_list_url, {"text": "A new list item"})

    def test_can_save_a_POST_request_to_an_existing_list(self, success_response, list):
        saved_items = Item.objects
        assert saved_items.count() == 1

        saved_item = saved_items.first()
        assert saved_item.text == "A new list item"
        assert saved_item.list == list

    def test_redirects_to_list_view(self, success_response, view_list_url, assert_redirects):
        assert_redirects(success_response, view_list_url)

    @pytest.fixture
    def invalid_form_response(self, client, view_list_url, mock_item_form_instance):
        """
        A response to a POST request to the view list page with invalid input.
        """
        mock_item_form_instance.is_valid.return_value = False
        return client.post(view_list_url, {"text": "A new list item."})

    def test_invalid_form_called_with_data_and_list(self, invalid_form_response, mock_item_form, list):
        mock_item_form.assert_called_with(invalid_form_response.wsgi_request.POST, list_=list)

    def test_invalid_form_renders_list_template(self, invalid_form_response, assert_template_used, list_template):
        assert invalid_form_response.status_code == 200
        assert_template_used(invalid_form_response, list_template)

    def test_invalid_form_passes_list_to_template(self, invalid_form_response, list):
        assert invalid_form_response.context["list"] == list

    def test_invalid_form_passes_form_to_template(self, invalid_form_response, mock_item_form_instance):
        assert invalid_form_response.context["form"] == mock_item_form_instance

    def test_invalid_form_doesnt_save(self, invalid_form_response, mock_item_form_instance):
        mock_item_form_instance.save.assert_not_called()


@pytest.fixture
def home_template():
    """Template that the home page uses."""
    return "lists/home.html"


class TestHome:
    @pytest.fixture
    def get_response(self, client, home_url):
        """Response to a GET request for the home page."""
        return client.get(home_url)

    def test_uses_home_template(self, get_response, assert_template_used, home_template):
        assert_template_used(get_response, home_template)

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
    def invalid_form_response(self, client, new_list_url, mock_item_form_instance):
        """
        A response to a POST request to the new list view with invalid input.
        """
        mock_item_form_instance.is_valid.return_value = False
        return client.post(new_list_url, {"text": "A new list item."})

    def test_invalid_form_called_with_data(self, invalid_form_response, mock_item_form):
        mock_item_form.assert_called_with(invalid_form_response.wsgi_request.POST)

    def test_invalid_form_doesnt_save(self, invalid_form_response, mock_item_form_instance):
        mock_item_form_instance.save.assert_not_called()

    def test_invalid_form_renders_home_template(self, invalid_form_response, assert_template_used, home_template):
        assert invalid_form_response.status_code == 200
        assert_template_used(invalid_form_response, home_template)

    def test_invalid_form_passes_form_to_template(self, invalid_form_response, mock_item_form_instance):
        assert invalid_form_response.context["form"] == mock_item_form_instance
