from unittest import mock

import pytest

from lists.forms import ItemForm
from lists.models import Item, List
from lists.views import new_list


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


@pytest.fixture
def new_list_url():
    """URL of the new list view."""
    return "/lists/new/"


@pytest.mark.django_db
class TestNewListIntegrated:
    def test_can_save_POST_request(self, client, new_list_url):
        client.post(new_list_url, data={"text": "A new list item"})
        assert Item.objects.count() == 1
        assert List.objects.count() == 1
        saved_item = Item.objects.first()
        saved_list = List.objects.first()
        assert saved_item.text == "A new list item"
        assert saved_item.list == saved_list

    def test_invalid_list_items_arent_saved(self, client, new_list_url):
        client.post(new_list_url, {"text": ""})
        assert Item.objects.count() == 0
        assert List.objects.count() == 0

    def test_list_owner_is_saved_if_user_is_authenticated(self, client, user, new_list_url):
        client.force_login(user)
        client.post(new_list_url, {"text": "new list item"})
        assert List.objects.first().owner == user


class TestNewListUnit:
    @pytest.fixture
    def mock_NewListForm(self, mocker):
        """A mock NewListForm class."""
        return mocker.patch("lists.views.NewListForm")

    @pytest.fixture
    def mock_redirect(self, mocker):
        """A mock redirect."""
        return mocker.patch("lists.views.redirect")

    @pytest.fixture
    def mock_render(self, mocker):
        """A mock render."""
        return mocker.patch("lists.views.render")

    @pytest.fixture
    def mock_form(self, mock_NewListForm):
        """A mock NewListForm instance."""
        return mock_NewListForm.return_value

    @pytest.fixture
    def post_request(self, new_list_url, rf, mock_redirect):
        """A POST request to the new list view."""
        request = rf.post(new_list_url, {"text": "new item text"})
        request.user = mock.Mock()
        return request

    @pytest.fixture
    def form_valid_request(self, post_request, mock_form):
        """A POST request to the new list view where the form is valid."""
        mock_form.is_valid.return_value = True
        return post_request

    def test_passes_POST_data_to_NewListForm(self, post_request, mock_NewListForm):
        new_list(post_request)

        mock_NewListForm.assert_called_once_with(data=post_request.POST)

    def test_saves_form_with_owner_if_form_valid(self, form_valid_request, mock_form):
        new_list(form_valid_request)

        mock_form.save.assert_called_once_with(owner=form_valid_request.user)

    def test_redirects_to_form_returned_object_if_form_valid(self, post_request, mock_form, mock_redirect):
        response = new_list(post_request)

        assert response == mock_redirect.return_value
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @pytest.fixture
    def form_invalid_request(self, post_request, mock_form):
        """A POST request to the new list view where the form is valid."""
        mock_form.is_valid.return_value = False
        return post_request

    def test_does_not_save_if_form_invalid(self, form_invalid_request, mock_form):
        new_list(form_invalid_request)

        mock_form.save.assert_not_called()

    def test_renders_home_template_with_form_if_form_invalid(
        self, form_invalid_request, mock_render, home_template, mock_form
    ):
        response = new_list(form_invalid_request)

        assert response == mock_render.return_value
        mock_render.assert_called_once_with(form_invalid_request, home_template, {"form": mock_form})


class TestMyLists:
    @pytest.fixture
    def get_response(self, client, user):
        """Response to a GET request for a user's lists."""
        return client.get(f"/lists/users/{user.email}/")

    @pytest.mark.django_db
    def test_my_lists_url_renders_my_lists_template(self, get_response, assert_template_used):
        assert_template_used(get_response, "lists/my_lists.html")

    @pytest.mark.django_db
    def test_passes_owner_to_template(self, get_response, user):
        assert get_response.context["owner"] == user
