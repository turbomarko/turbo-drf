import json

from django.conf import settings
from django.test import TestCase
from django.test.client import MULTIPART_CONTENT, Client
from django.urls import reverse
from django.utils.encoding import force_str
from rest_framework import permissions, status


class CustomPermissionClass(permissions.BasePermission):
    message = "You shall not pass!"

    def has_permission(self, request, view):
        return False


class APIClient(Client):
    def patch(
        self, path, data="", content_type=MULTIPART_CONTENT, follow=False, **extra
    ):
        return self.generic("PATCH", path, data, content_type, **extra)

    def options(
        self, path, data="", content_type=MULTIPART_CONTENT, follow=False, **extra
    ):
        return self.generic("OPTIONS", path, data, content_type, **extra)


class TestsMixin(TestCase):
    """
    base for API tests:
        * easy request calls, f.e.: self.post(url, data), self.get(url)
        * easy status check, f.e.: self.post(url, data, status_code=200)
    """

    PASS = "person"
    EMAIL = "person1@world.com"
    NEW_PASS = "new-test-pass"

    # data without user profile
    REGISTRATION_DATA = {
        "email": EMAIL,
        "password": NEW_PASS,
    }

    BASIC_USER_DATA = {
        "first_name": "John",
        "last_name": "Smith",
        "email": EMAIL,
    }

    def send_request(self, request_method, *args, **kwargs):
        request_func = getattr(self.client, request_method)
        status_code = None
        if "content_type" not in kwargs and request_method != "get":
            kwargs["content_type"] = "application/json"
        if (
            "data" in kwargs
            and request_method != "get"
            and kwargs["content_type"] == "application/json"
        ):
            data = kwargs.get("data", "")
            kwargs["data"] = json.dumps(data)  # , cls=CustomJSONEncoder
        if "status_code" in kwargs:
            status_code = kwargs.pop("status_code")

        self.response = request_func(*args, **kwargs)
        is_json = "application/json" in self.response.get("content-type", "")

        self.response.json = {}
        if is_json and self.response.content:
            self.response.json = json.loads(force_str(self.response.content))

        if status_code:
            self.assertEqual(self.response.status_code, status_code)

        return self.response

    def post(self, *args, **kwargs):
        return self.send_request("post", *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.send_request("get", *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.send_request("patch", *args, **kwargs)

    def init(self):
        settings.DEBUG = True
        self.client = APIClient()

        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.password_change_url = reverse("rest_password_change")
        self.register_url = reverse("register")
        self.password_reset_url = reverse("password_reset")
        self.user_url = reverse("user-detail")
        self.verify_email_url = reverse("verify_email")
        self.resend_email_url = reverse("resend_email")

    def _login(self, pw=None, expected_status_code=status.HTTP_200_OK):
        payload = {
            "email": self.EMAIL,
            "password": pw if pw is not None else self.PASS,
        }
        self.post(self.login_url, data=payload, status_code=expected_status_code)

    def _logout(self):
        self.post(self.logout_url, status=status.HTTP_200_OK)
