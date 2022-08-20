from rest_framework.test import APIRequestFactory

from ..models import User
from ..views import UserViewSet


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: APIRequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: APIRequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        response = view.me(request)  # type:ignore

        assert response.data == {
            "id": str(user.id),
            "email": user.email,
            "url": f"http://testserver/api/users/{user.id}/",
        }
