from allauth.account import app_settings as account_app_settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from django.utils.encoding import force_str
from rest_framework import status

from .mixins import TestsMixin


@override_settings(ROOT_URLCONF="api.users.tests.urls")
class APIBasicTests(TestsMixin):
    """
    Class for running tests
    """

    def setUp(self):
        self.init()

    def _generate_uid_and_token(self, user):
        result = {}
        from allauth.account.forms import default_token_generator
        from allauth.account.utils import user_pk_to_url_str

        result["uid"] = user_pk_to_url_str(user)

        result["token"] = default_token_generator.make_token(user)
        return result

    @override_settings(
        ACCOUNT_AUTHENTICATION_METHOD=account_app_settings.AuthenticationMethod.EMAIL
    )
    def test_login_failed_email_validation(self):
        payload = {
            "email": "",
            "password": self.PASS,
        }

        resp = self.post(self.login_url, data=payload, status_code=400)
        self.assertEqual(resp.json["email"], ["This field may not be blank."])

    @override_settings(
        ACCOUNT_AUTHENTICATION_METHOD=account_app_settings.AuthenticationMethod.EMAIL
    )
    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_allauth_login_with_email(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }
        # there is no users in db so it should throw error (400)
        self.post(self.login_url, data=payload, status_code=400)

        self.post(self.password_change_url, status_code=401)

        # create user
        get_user_model().objects.create_user(self.EMAIL, self.PASS)

        self.post(self.login_url, data=payload, status_code=200)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_password_change_with_old_password(self):
        login_payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }
        get_user_model().objects.create_user(self.EMAIL, self.PASS)
        self.post(self.login_url, data=login_payload, status_code=200)

        new_password_payload = {
            "old_password": f"{self.PASS}!",  # wrong password
            "new_password": "new_person",
        }
        self.post(
            self.password_change_url,
            data=new_password_payload,
            status_code=400,
        )

        new_password_payload = {
            "old_password": self.PASS,
            "new_password": "dhgfvdufzuvzvh",
        }
        self.post(
            self.password_change_url,
            data=new_password_payload,
            status_code=200,
        )

        # user should not be able to login using old password
        self.post(self.login_url, data=login_payload, status_code=400)

        # new password should work
        login_payload["password"] = new_password_payload["new_password"]
        self.post(self.login_url, data=login_payload, status_code=200)

    def _password_reset(self):
        user = get_user_model().objects.create_user(self.EMAIL, self.PASS)

        # call password reset
        mail_count = len(mail.outbox)
        payload = {"email": self.EMAIL}
        self.post(self.password_reset_url, data=payload, status_code=200)
        self.assertEqual(len(mail.outbox), mail_count + 1)

        url_kwargs = self._generate_uid_and_token(user)
        url = reverse("password_reset_confirm")

        # wrong token
        data = {
            "new_password": self.NEW_PASS,
            "uid": force_str(url_kwargs["uid"]),
            "token": "-wrong-token-",
        }
        self.post(url, data=data, status_code=400)

        # wrong uid
        data = {
            "new_password": self.NEW_PASS,
            "uid": "-wrong-uid-",
            "token": url_kwargs["token"],
        }
        self.post(url, data=data, status_code=400)

        # wrong token and uid
        data = {
            "new_password": self.NEW_PASS,
            "uid": "-wrong-uid-",
            "token": "-wrong-token-",
        }
        self.post(url, data=data, status_code=400)

        # valid payload
        data = {
            "new_password": self.NEW_PASS,
            "uid": force_str(url_kwargs["uid"]),
            "token": url_kwargs["token"],
        }
        url = reverse("password_reset_confirm")
        self.post(url, data=data, status_code=200)

        payload = {
            "email": self.EMAIL,
            "password": self.NEW_PASS,
        }
        self.post(self.login_url, data=payload, status_code=200)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_password_reset_allauth(self):
        self._password_reset()

    def test_password_reset_with_email_in_different_case(self):
        get_user_model().objects.create_user(self.EMAIL.lower(), self.PASS)

        # call password reset in upper case
        mail_count = len(mail.outbox)
        payload = {"email": self.EMAIL.upper()}
        self.post(self.password_reset_url, data=payload, status_code=200)
        self.assertEqual(len(mail.outbox), mail_count + 1)

    def test_password_reset_with_invalid_email(self):
        """
        Invalid email should not raise error, as this would leak users
        """
        get_user_model().objects.create_user(self.EMAIL, self.PASS)

        # call password reset
        mail_count = len(mail.outbox)
        payload = {"email": "nonexisting@email.com"}
        self.post(self.password_reset_url, data=payload, status_code=200)
        self.assertEqual(len(mail.outbox), mail_count)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_user_details_using_jwt(self):
        user = get_user_model().objects.create_user(self.EMAIL, self.PASS)
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }
        self.post(self.login_url, data=payload, status_code=200)
        self.get(self.user_url, status_code=200)

        self.patch(self.user_url, data=self.BASIC_USER_DATA, status_code=200)
        user = get_user_model().objects.get(pk=user.pk)
        self.assertEqual(user.email, self.response.json["email"])

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_registration_with_jwt(self):
        user_count = get_user_model().objects.all().count()

        self.post(self.register_url, data={}, status_code=400)

        resp = self.post(
            self.register_url, data=self.REGISTRATION_DATA, status_code=201
        )
        self.assertIn("access-token", resp.cookies)
        self.assertEqual(get_user_model().objects.all().count(), user_count + 1)

        self._login(pw=self.NEW_PASS)
        self._logout()

    def test_registration_with_invalid_password(self):
        data = self.REGISTRATION_DATA.copy()
        data["password"] = "abc123"

        self.post(self.register_url, data=data, status_code=400)

    @override_settings(
        ACCOUNT_EMAIL_VERIFICATION="mandatory",
        ACCOUNT_EMAIL_REQUIRED=True,
        ACCOUNT_EMAIL_CONFIRMATION_HMAC=False,
    )
    def test_registration_with_email_verification(self):
        user_count = get_user_model().objects.all().count()
        mail_count = len(mail.outbox)

        # test empty payload
        self.post(
            self.register_url,
            data={},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        resp = self.post(
            self.register_url,
            data=self.REGISTRATION_DATA,
            status_code=status.HTTP_201_CREATED,
        )

        self.assertNotIn("access-token", resp.cookies.keys())
        self.assertEqual(get_user_model().objects.all().count(), user_count + 1)
        self.assertEqual(len(mail.outbox), mail_count + 1)
        new_user = get_user_model().objects.latest("id")
        self.assertEqual(new_user.email, self.REGISTRATION_DATA["email"])

        # increment count
        mail_count += 1

        # test browsable endpoint
        resp = self.get(
            self.verify_email_url, status_code=status.HTTP_405_METHOD_NOT_ALLOWED
        )
        self.assertEqual(resp.json["detail"], 'Method "GET" not allowed.')

        # email is not verified yet
        payload = {
            "email": self.EMAIL,
            "password": self.NEW_PASS,
        }
        self.post(
            self.login_url,
            data=payload,
            status=status.HTTP_400_BAD_REQUEST,
        )

        # resend email
        self.post(
            self.resend_email_url,
            data={"email": self.EMAIL},
            status_code=status.HTTP_200_OK,
        )
        # check mail count
        self.assertEqual(len(mail.outbox), mail_count + 1)

        # verify email
        email_confirmation = new_user.emailaddress_set.get(
            email=self.EMAIL
        ).emailconfirmation_set.order_by("-created")[0]
        self.post(
            self.verify_email_url,
            data={"key": email_confirmation.key},
            status_code=status.HTTP_200_OK,
        )
        new_user.refresh_from_db()
        # try to login again
        self._login(pw=self.NEW_PASS)
        self._logout()

    def test_should_not_resend_email_verification_for_nonexistent_email(self):
        # mail count before resend
        mail_count = len(mail.outbox)

        # resend non-existent email
        resend_email_result = self.post(
            self.resend_email_url,
            data={"email": "test@test.com"},
            status_code=status.HTTP_200_OK,
        )

        self.assertEqual(resend_email_result.status_code, status.HTTP_200_OK)
        # verify that mail count did not increment
        self.assertEqual(mail_count, len(mail.outbox))

    @override_settings(ACCOUNT_LOGOUT_ON_GET=True)
    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_logout_on_get(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }

        # create user
        get_user_model().objects.create_user(self.EMAIL, self.PASS)

        self.post(self.login_url, data=payload, status_code=200)
        self.get(self.logout_url, status=status.HTTP_200_OK)

    @override_settings(ACCOUNT_LOGOUT_ON_GET=False)
    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_logout_on_post_only(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }

        # create user
        get_user_model().objects.create_user(self.EMAIL, self.PASS)

        self.post(self.login_url, data=payload, status_code=status.HTTP_200_OK)
        self.get(self.logout_url, status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_login_jwt_sets_cookie(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }
        get_user_model().objects.create_user(self.EMAIL, self.PASS)
        resp = self.post(self.login_url, data=payload, status_code=200)
        self.assertTrue("access-token" in resp.cookies.keys())

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_logout_jwt_deletes_cookie(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }
        get_user_model().objects.create_user(self.EMAIL, self.PASS)
        self.post(self.login_url, data=payload, status_code=200)
        resp = self.post(self.logout_url, status=200)
        self.assertEqual("", resp.cookies.get("access-token").value)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_logout_jwt_deletes_cookie_refresh(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }
        get_user_model().objects.create_user(self.EMAIL, self.PASS)
        self.post(self.login_url, data=payload, status_code=200)
        resp = self.post(self.logout_url, status=200)
        self.assertEqual("", resp.cookies.get("access-token").value)
        self.assertEqual("", resp.cookies.get("refresh-token").value)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_cookie_authentication(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }
        get_user_model().objects.create_user(self.EMAIL, self.PASS)
        resp = self.post(self.login_url, data=payload, status_code=200)
        self.assertEqual(["access-token", "refresh-token"], list(resp.cookies.keys()))
        resp = self.get(self.user_url, status_code=200)
        self.assertEqual(resp.status_code, 200)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_blacklisting(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }
        get_user_model().objects.create_user(self.EMAIL, self.PASS)
        resp = self.post(self.login_url, data=payload, status_code=200)
        token = resp.cookies.get("refresh-token").value
        # test successful logout
        self.post(self.logout_url, status_code=200, data={"refresh": token})
        # test token is blacklisted
        self.post(self.logout_url, status_code=401, data={"refresh": token})

    @override_settings(JWT_AUTH_COOKIE_USE_CSRF=False)
    @override_settings(CSRF_COOKIE_SECURE=True)
    @override_settings(CSRF_COOKIE_HTTPONLY=True)
    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_wo_csrf_enforcement(self):
        from .mixins import APIClient

        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }
        client = APIClient(enforce_csrf_checks=True)
        get_user_model().objects.create_user(self.EMAIL, self.PASS)

        resp = client.post(self.login_url, payload)
        self.assertTrue("access-token" in list(client.cookies.keys()))
        self.assertEqual(resp.status_code, 200)

        # TEST WITH COOKIES
        resp = client.get("/protected-view/")
        self.assertEqual(resp.status_code, 200)

        resp = client.post("/protected-view/", {})
        self.assertEqual(resp.status_code, 200)

    @override_settings(JWT_AUTH_COOKIE_USE_CSRF=True)
    @override_settings(CSRF_COOKIE_SECURE=True)
    @override_settings(CSRF_COOKIE_HTTPONLY=True)
    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_csrf_wo_login_csrf_enforcement(self):
        from .mixins import APIClient

        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }
        client = APIClient(enforce_csrf_checks=True)
        get_user_model().objects.create_user(self.EMAIL, self.PASS)

        client.get(reverse("getcsrf"))
        csrftoken = client.cookies["csrftoken"].value

        resp = client.post(self.login_url, payload)
        self.assertTrue("access-token" in list(client.cookies.keys()))
        self.assertTrue("csrftoken" in list(client.cookies.keys()))
        self.assertEqual(resp.status_code, 200)

        # TEST WITH COOKIES
        resp = client.get("/protected-view/")
        self.assertEqual(resp.status_code, 200)
        # fail w/o csrftoken in payload
        resp = client.post("/protected-view/", {})
        self.assertEqual(resp.status_code, 403)

        csrfparam = {"csrfmiddlewaretoken": csrftoken}
        resp = client.post("/protected-view/", csrfparam)
        self.assertEqual(resp.status_code, 200)

    @override_settings(JWT_AUTH_RETURN_EXPIRATION=True)
    @override_settings(JWT_AUTH_COOKIE="xxx")
    @override_settings(ACCOUNT_LOGOUT_ON_GET=True)
    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_refresh_cookie_name(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }

        # create user
        get_user_model().objects.create_user(self.EMAIL, self.PASS)

        resp = self.post(self.login_url, data=payload, status_code=200)
        self.assertIn("xxx", resp.cookies.keys())
        self.assertIn("refresh-token", resp.cookies.keys())
        self.assertEqual(resp.cookies.get("refresh-token").get("path"), "/auth/token")

    @override_settings(JWT_AUTH_RETURN_EXPIRATION=True)
    @override_settings(JWT_AUTH_COOKIE="xxx")
    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_custom_token_refresh_view(self):
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }

        get_user_model().objects.create_user(self.EMAIL, self.PASS)
        resp = self.post(self.login_url, data=payload, status_code=200)
        refresh = resp.data.get("refresh-token")
        refresh_resp = self.post(
            reverse("token_refresh"),
            data=dict(refresh=refresh),
            status_code=200,
        )
        self.assertIn("xxx", refresh_resp.cookies)

    @override_settings(ACCOUNT_EMAIL_VERIFICATION="optional")
    def test_rotate_token_refresh_view(self):
        from rest_framework_simplejwt.settings import api_settings as jwt_settings

        jwt_settings.ROTATE_REFRESH_TOKENS = True
        payload = {
            "email": self.EMAIL,
            "password": self.PASS,
        }

        get_user_model().objects.create_user(self.EMAIL, self.PASS)
        resp = self.post(self.login_url, data=payload)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        refresh = resp.data.get("refresh_token", None)
        resp = self.post(
            reverse("token_refresh"),
            data=dict(refresh=refresh),
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("refresh-token", resp.cookies.keys())
