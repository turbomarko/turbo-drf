from django.urls import path

from rest_framework_simplejwt.views import TokenVerifyView

from .views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    RegisterView,
    ResendEmailVerificationView,
    UserDetailsView,
    VerifyEmailView,
)
from .jwt import get_refresh_view


# Authentication urls
urlpatterns = [
    # URLs that do not require a session or valid token
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("login/", LoginView.as_view(), name="login"),
    # URLs that require a user to be logged in with a valid token.
    path("token/logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserDetailsView.as_view(), name="user-detail"),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
]

# Registration urls
urlpatterns = [
    path("registration/", RegisterView.as_view(), name="register"),
    path(
        "registration/verify-email/",
        VerifyEmailView.as_view(),
        name="verify_email",
    ),
    path(
        "registration/resend-email/",
        ResendEmailVerificationView.as_view(),
        name="resend_email",
    ),
    # account_confirm_email - You should override this view to handle it in
    # your API client somehow and then, send post to /verify-email/ endpoint
    # with proper key.
    # If you don't want to use API on that step, then just use ConfirmEmailView
    # view from:
    # https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py
    # re_path(
    #     r"^registration/account-confirm-email/(?P<key>[-:\w]+)/$", TemplateView.as_view(),
    #     name="account_confirm_email",
    # ),
    # # This url is used by django-allauth and empty TemplateView is
    # # defined just to allow reverse() call inside app, for example when email
    # # with verification link is being sent, then it's required to render email
    # # content.
    # path(
    #     "registration/account-email-verification-sent/", TemplateView.as_view(),
    #     name="account_email_verification_sent",
    # ),
] + urlpatterns
