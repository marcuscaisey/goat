import pytest

from users.forms import AuthenticationForm


class TestLoginView:
    @pytest.fixture
    def get_response(self, client):
        """Response to a GET request to the login page."""
        return client.get("/login/")

    def test_uses_login_template(self, get_response, assert_template_used):
        assert_template_used(get_response, "users/login.html")

    def test_passes_authentication_form_to_template(self, get_response):
        assert isinstance(get_response.context["form"], AuthenticationForm)

    @pytest.fixture
    def success_response(self, client, user):
        """Response to a successful login POST request."""
        return client.post("/login/", {"username": user.email, "password": user.raw_password})

    @pytest.mark.django_db
    def test_user_can_login(self, success_response):
        assert success_response.wsgi_request.user.is_authenticated

    @pytest.mark.django_db
    def test_successful_login_redirects_to_home_page(self, success_response, assert_redirects):
        assert_redirects(success_response, "/")

    @pytest.fixture(params=["email", "password", "both"])
    def fail_response(self, request, client, user):
        """
        Response to a failed login POST request with either email incorrect,
        password incorrect, or both.
        """
        email = f"incorrect-{user.email}" if request.param in ("email", "both") else user.email
        password = f"incorrect-{user.raw_password}" if request.param in ("password", "both") else user.raw_password
        return client.post("/login/", {"username": email, "password": password})

    @pytest.mark.django_db
    def test_failure_to_login_renders_login_template(self, fail_response, assert_template_used):
        assert fail_response.status_code == 200
        assert_template_used(fail_response, "users/login.html")

    @pytest.mark.django_db
    def test_failure_to_login_passes_authentication_form_to_template(self, fail_response):
        assert isinstance(fail_response.context["form"], AuthenticationForm)


class TestLogoutView:
    @pytest.fixture
    def response(self, client, user):
        """Response to a logged in user logging out."""
        client.force_login(user)
        return client.get("/logout/")

    @pytest.mark.django_db
    def test_user_can_logout(self, response):
        assert not response.wsgi_request.user.is_authenticated

    @pytest.mark.django_db
    def test_redirects_to_home_page(self, response, assert_redirects):
        assert_redirects(response, "/")

    @pytest.fixture
    def logged_out_user_response(self, client):
        """Response to a logged out user logging out."""
        return client.get("/logout/")

    def test_logged_out_user_redirects_to_home_page(self, logged_out_user_response, assert_redirects):
        assert_redirects(logged_out_user_response, "/")
