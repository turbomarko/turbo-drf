from allauth.account import app_settings as allauth_settings
from allauth.account.models import EmailAddress
from allauth.account.utils import complete_signup
from allauth.account.views import ConfirmEmailView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


from .jwt import extract_refresh_token, jwt_encode, set_jwt_cookies, unset_jwt_cookies

from .serializers import (
    LoginSerializer,
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
    ResendEmailVerificationSerializer,
    UserSerializer,
    VerifyEmailSerializer,
)

User = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        "password", "password1", "old_password", "new_password", "new_password1"
    ),
)


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    throttle_scope = "auth"

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if (
            allauth_settings.EMAIL_VERIFICATION
            == allauth_settings.EmailVerificationMethod.MANDATORY
        ):
            return {"info": "Verification e-mail sent."}

        return UserSerializer(user, context=self.get_serializer_context()).data

    def perform_create(self, serializer):
        user = serializer.save(self.request)

        complete_signup(
            self.request._request,
            user,
            allauth_settings.EMAIL_VERIFICATION,
            None,
        )
        return user

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        if data:
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
            if (
                allauth_settings.EMAIL_VERIFICATION
                != allauth_settings.EmailVerificationMethod.MANDATORY
            ):
                access_token, refresh_token = jwt_encode(user)
                set_jwt_cookies(response, access_token, refresh_token)
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response


class VerifyEmailView(APIView, ConfirmEmailView):
    permission_classes = (AllowAny,)
    allowed_methods = ["POST", "OPTIONS", "HEAD"]

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)

    def get(self, *args, **kwargs):
        raise MethodNotAllowed("GET")

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs["key"] = serializer.validated_data["key"]
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({"success": "Your email address has been verified"})


class ResendEmailVerificationView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResendEmailVerificationSerializer
    queryset = EmailAddress.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = EmailAddress.objects.filter(**serializer.validated_data).first()
        if email and not email.verified:
            email.send_confirmation(request)

        return Response(status=status.HTTP_200_OK)


class LoginView(GenericAPIView):
    """
    Returns the user object and sets the JWT cookies if the credentials are valid.
    Calls Django Auth login method to register User ID in Django session framework.
    """

    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    throttle_scope = "auth"

    access_token = None

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_response(self, user):
        serializer = UserSerializer(
            instance=user,
            context=self.get_serializer_context(),
        )

        response = Response(serializer.data, status=status.HTTP_200_OK)
        set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=request.data)
        self.serializer.is_valid(raise_exception=True)

        user = self.serializer.validated_data["user"]
        self.access_token, self.refresh_token = jwt_encode(user)
        return self.get_response(user)


class LogoutView(APIView):
    """Removes the JWT auth cookies from the browser"""

    permission_classes = (IsAuthenticated,)
    throttle_scope = "auth"

    def post(self, request, *args, **kwargs):
        response = Response(
            {"success": "Successfully logged out"},
            status=status.HTTP_200_OK,
        )

        unset_jwt_cookies(response)

        if "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS:
            # add refresh token to blacklist
            try:
                token = RefreshToken(extract_refresh_token(request))
                token.blacklist()
            except (TokenError, AttributeError, TypeError) as error:
                if hasattr(error, "args"):
                    if (
                        "Token is blacklisted" in error.args
                        or "Token is invalid or expired" in error.args
                    ):
                        response.data = {"error": error.args[0]}
                        response.status_code = status.HTTP_401_UNAUTHORIZED
                    else:
                        response.data = {"error": "An error has occurred."}
                        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

                else:
                    response.data = {"error": "An error has occurred."}
                    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return response


class UserDetailsView(RetrieveUpdateAPIView):
    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods
    """

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using django-rest-swagger
        """
        return User.objects.none()


class PasswordResetView(GenericAPIView):
    """Calls Django Auth PasswordResetForm save method"""

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)
    throttle_scope = "auth"

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response({"info": "Password reset e-mail has been sent"})


class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)
    throttle_scope = "auth"

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "Your password has been renewed"})


class PasswordChangeView(GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)
    throttle_scope = "auth"

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": "The new password has been saved"})
