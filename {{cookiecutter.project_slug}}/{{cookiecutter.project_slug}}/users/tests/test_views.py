from rest_framework.test import APIRequestFactory

from ..models import User
from ..views import UserDetailsView


class TestUserViewSet:
    def test_get_user(self, user: User, rf: APIRequestFactory):
        view = UserDetailsView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user == view.get_object()
