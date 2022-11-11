from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import CSRFCheck
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.settings import api_settings as jwt_settings


def jwt_encode(user):
    refresh = TokenObtainPairSerializer.get_token(user)
    return refresh.access_token, refresh


def set_jwt_access_cookie(response, access_token):
    cookie_name = getattr(settings, "JWT_AUTH_COOKIE", None)
    access_token_expiration = timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME
    cookie_secure = getattr(settings, "JWT_AUTH_SECURE", False)
    cookie_httponly = getattr(settings, "JWT_AUTH_HTTPONLY", True)
    cookie_samesite = getattr(settings, "JWT_AUTH_SAMESITE", "Lax")

    if cookie_name:
        response.set_cookie(
            cookie_name,
            access_token,
            expires=access_token_expiration,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
        )


def set_jwt_refresh_cookie(response, refresh_token):
    refresh_token_expiration = timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME
    refresh_cookie_name = getattr(settings, "JWT_AUTH_REFRESH_COOKIE", None)
    refresh_cookie_path = getattr(
        settings, "JWT_AUTH_REFRESH_COOKIE_PATH", "/auth/token"
    )
    cookie_secure = getattr(settings, "JWT_AUTH_SECURE", False)
    cookie_httponly = getattr(settings, "JWT_AUTH_HTTPONLY", True)
    cookie_samesite = getattr(settings, "JWT_AUTH_SAMESITE", "Lax")

    if refresh_cookie_name:
        response.set_cookie(
            refresh_cookie_name,
            refresh_token,
            expires=refresh_token_expiration,
            secure=cookie_secure,
            httponly=cookie_httponly,
            samesite=cookie_samesite,
            path=refresh_cookie_path,
        )


def set_jwt_cookies(response, access_token, refresh_token):
    set_jwt_access_cookie(response, access_token)
    set_jwt_refresh_cookie(response, refresh_token)


def unset_jwt_cookies(response):
    cookie_name = getattr(settings, "JWT_AUTH_COOKIE", None)
    refresh_cookie_name = getattr(settings, "JWT_AUTH_REFRESH_COOKIE", None)
    refresh_cookie_path = getattr(
        settings, "JWT_AUTH_REFRESH_COOKIE_PATH", "/auth/token"
    )

    if cookie_name:
        response.delete_cookie(cookie_name, samesite=None)
    if refresh_cookie_name:
        response.delete_cookie(
            refresh_cookie_name, path=refresh_cookie_path, samesite=None
        )


def extract_refresh_token(request):
    cookie_name = getattr(settings, "JWT_AUTH_REFRESH_COOKIE", None)
    if cookie_name and cookie_name in request.COOKIES:
        return request.COOKIES.get(cookie_name)
    else:
        raise InvalidToken("No valid refresh token found.")


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = extract_refresh_token(self.context["request"])
        return super().validate(attrs)


def get_refresh_view():
    """Returns a Token Refresh CBV without a circular import"""
    from rest_framework_simplejwt.views import TokenRefreshView

    class RefreshViewWithCookieSupport(TokenRefreshView):
        serializer_class = CookieTokenRefreshSerializer

        def finalize_response(self, request, response, *args, **kwargs):
            if response.status_code == 200:
                set_jwt_cookies(
                    response, response.data["access"], response.data["refresh"]
                )
                response.data = {}
            else:
                unset_jwt_cookies(response)
            return super().finalize_response(request, response, *args, **kwargs)

    return RefreshViewWithCookieSupport


class JWTCookieAuthentication(JWTAuthentication):
    """
    An authentication plugin that hopefully authenticates requests through a JSON web
    token provided in a request cookie (and through the header as normal, with a
    preference to the header).
    """

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation for session based authentication.
        """

        def dummy_get_response(request):  # pragma: no cover
            return None

        check = CSRFCheck(dummy_get_response)
        # populates request.META["CSRF_COOKIE"], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied(f"CSRF Failed: {reason}")

    def authenticate(self, request):
        cookie_name = getattr(settings, "JWT_AUTH_COOKIE", None)
        header = self.get_header(request)
        if header is None:
            if cookie_name:
                raw_token = request.COOKIES.get(cookie_name)
                if raw_token is not None and getattr(
                    settings, "JWT_AUTH_COOKIE_USE_CSRF", False
                ):
                    self.enforce_csrf(request)
            else:
                return None
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
