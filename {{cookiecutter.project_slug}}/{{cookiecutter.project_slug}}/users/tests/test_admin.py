import pytest
from django.urls import reverse

from ..models import User
from .factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserAdmin:
    def test_changelist(self, admin_client):
        """
        Tests UserAdmin changelist view
        """

        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200

    def test_search(self, admin_client):
        """
        Tests UserAdmin changelist search functionality
        """

        url = reverse("admin:users_user_changelist")
        response = admin_client.get(url, data={"q": "test"})
        assert response.status_code == 200

    def test_add(self, admin_client):
        """
        Tests UserAdmin user creation
        """

        url = reverse("admin:users_user_add")
        response = admin_client.get(url)
        assert response.status_code == 200

        user = UserFactory.build()
        response = admin_client.post(
            url,
            data={
                "email": user.email,
                "password1": user.password,
                "password2": user.password,
            },
        )
        assert response.status_code == 302
        assert User.objects.filter(email=user.email).exists()

    def test_view_user(self, admin_client):
        """
        Tests UserAdmin user editor view
        """

        user = UserFactory()
        url = reverse("admin:users_user_change", kwargs={"object_id": user.pk})
        response = admin_client.get(url)
        assert response.status_code == 200
