from django.urls import resolve, reverse

from ..models import User


def test_user_detail(user: User):
    assert reverse("api:user-detail") == "/auth/user/"
    assert resolve("/auth/user/").view_name == "api:user-detail"
