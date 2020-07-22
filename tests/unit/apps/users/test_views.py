import pytest

from users.forms import AuthenticationForm


class TestLoginView:
    @pytest.fixture
    def login_template(self):
        """Template that the login page uses."""
        return "users/login.html"

    @pytest.fixture
    def get_response(self, client, login_url):
        """Response to a GET request to the login page."""
        return client.get(login_url)

    def test_uses_login_template(self, get_response, assert_template_used, login_template):
        assert_template_used(get_response, login_template)

    def test_passes_authentication_form_to_template(self, get_response):
        assert isinstance(get_response.context["form"], AuthenticationForm)

    @pytest.fixture
    def success_response(self, client, user, login_url):
        """Response to a successful login POST request."""
        return client.post(login_url, {"username": user.email, "password": user.raw_password})

    @pytest.mark.django_db
    def test_user_can_login(self, success_response):
        assert success_response.wsgi_request.user.is_authenticated

    @pytest.mark.django_db
    def test_successful_login_redirects_to_home_page(self, success_response, assert_redirects, home_url):
        assert_redirects(success_response, home_url)

    @pytest.fixture(params=["email", "password", "both"])
    def fail_response(self, request, client, user, login_url):
        """
        Response to a failed login POST request with either email incorrect,
        password incorrect, or both.
        """
        email = f"incorrect-{user.email}" if request.param in ("email", "both") else user.email
        password = f"incorrect-{user.raw_password}" if request.param in ("password", "both") else user.raw_password
        return client.post(login_url, {"username": email, "password": password})

    @pytest.mark.django_db
    def test_failure_to_login_renders_login_template(self, fail_response, assert_template_used, login_template):
        assert fail_response.status_code == 200
        assert_template_used(fail_response, login_template)

    @pytest.mark.django_db
    def test_failure_to_login_passes_authentication_form_to_template(
        self, fail_response, assert_form_is_instance_with_errors
    ):
        assert_form_is_instance_with_errors(fail_response.context["form"], AuthenticationForm)


class TestLogoutView:
    @pytest.fixture
    def logout_url(self):
        """URL of the logout page."""
        return "/logout/"

    @pytest.fixture
    def response(self, client, user, logout_url):
        """Response to a logged in user logging out."""
        client.force_login(user)
        return client.get(logout_url)

    @pytest.mark.django_db
    def test_user_can_logout(self, response):
        assert not response.wsgi_request.user.is_authenticated

    @pytest.mark.django_db
    def test_redirects_to_home_page(self, response, assert_redirects, home_url):
        assert_redirects(response, home_url)

    @pytest.fixture
    def logged_out_user_response(self, client, logout_url):
        """Response to a logged out user logging out."""
        return client.get(logout_url)

    def test_logged_out_user_redirects_to_home_page(self, logged_out_user_response, assert_redirects, home_url):
        assert_redirects(logged_out_user_response, home_url)
