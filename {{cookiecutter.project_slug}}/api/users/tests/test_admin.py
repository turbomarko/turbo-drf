from http import HTTPStatus
from importlib import reload

import pytest
from django.contrib import admin
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from ..models import User
from .factories import UserFactory


class TestUserAdmin:
    def test_changelist(self, admin_client):
        """
        Tests UserAdmin changelist view
        """

        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.OK

    def test_search(self, admin_client):
        """
        Tests UserAdmin changelist search functionality
        """

        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == HTTPStatus.OK

    def test_add(self, admin_client):
        """
        Tests UserAdmin user creation
        """

        url = reverse("admin:users_user_add")
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.OK

        user = UserFactory.build()
        response = admin_client.post(
            url,
            data={
                {%- if cookiecutter.username_type == "email" %}
                "email": user.email,
                {%- else %}
                "username": user.username,
                {%- endif %}
                "password1": user.password,
                "password2": user.password,
            },
        )
        assert response.status_code == HTTPStatus.FOUND
        {%- if cookiecutter.username_type == "email" %}
        assert User.objects.filter(email=user.email).exists()
        {%- else %}
        assert User.objects.filter(username=user.username).exists()
        {%- endif %}

    def test_view_user(self, admin_client):
        """
        Tests UserAdmin user editor view
        """

        user = UserFactory()
        url = reverse("admin:users_user_change", kwargs={"object_id": user.pk})
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.OK

    @pytest.fixture()
    def _force_allauth(self, settings):
        settings.DJANGO_ADMIN_FORCE_ALLAUTH = True
        # Reload the admin module to apply the setting change
        import api.users.admin as users_admin

        with contextlib.suppress(admin.sites.AlreadyRegistered):  # type: ignore[attr-defined]
            reload(users_admin)

    @pytest.mark.django_db()
    @pytest.mark.usefixtures("_force_allauth")
    def test_allauth_login(self, rf, settings):
        request = rf.get("/fake-url")
        request.user = AnonymousUser()
        response = admin.site.login(request)

        # The `admin` login view should redirect to the `allauth` login view
        target_url = reverse(settings.LOGIN_URL) + "?next=" + request.path
        assertRedirects(response, target_url, fetch_redirect_response=False)
