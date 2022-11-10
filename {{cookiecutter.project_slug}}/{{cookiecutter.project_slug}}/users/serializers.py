from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.urls import exceptions as url_exceptions
from django.utils.encoding import force_str

from rest_framework import exceptions, serializers
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from .forms import AllAuthPasswordResetForm

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        """Make the email lowercase"""
        return value.lower()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={"input_type": "password"})

    def get_auth_user(self, email, password):
        """
        Retrieve the auth user from given POST payload by using `allauth`

        Returns the authenticated user instance if credentials are correct,
        else `None` will be returned
        """
        # When `is_active` of a user is set to False, allauth tries to return template html
        # which does not exist. This is the solution for it. See issue #264.
        try:
            return authenticate(self.context["request"], email=email, password=password)
        except url_exceptions.NoReverseMatch:
            msg = "Unable to log in with provided credentials."
            raise exceptions.ValidationError(msg)

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = "User account is disabled."
            raise exceptions.ValidationError(msg)

    @staticmethod
    def validate_email_verification_status(user):
        from allauth.account.app_settings import (
            EMAIL_VERIFICATION,
            EmailVerificationMethod,
        )

        if (
            EMAIL_VERIFICATION == EmailVerificationMethod.MANDATORY
            and not user.emailaddress_set.filter(
                email=user.email, verified=True
            ).exists()
        ):
            raise serializers.ValidationError("E-mail is not verified.")

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = self.get_auth_user(email, password)

        if not user:
            msg = "Unable to log in with provided credentials."
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        self.validate_email_verification_status(user)

        data["user"] = user
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        """Make the email lowercase"""
        return value.lower()

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def get_cleaned_data(self):
        return {
            "email": self.validated_data.get("email", ""),
            "password1": self.validated_data.get("password", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        user.save()
        setup_user_email(request, user, [])
        return user


class VerifyEmailSerializer(serializers.Serializer):
    key = serializers.CharField()


class ResendEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for requesting a password reset e-mail"""

    email = serializers.EmailField()
    reset_form = None

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        return {}

    def validate_email(self, value):
        # Create PasswordResetForm with the serializer
        self.reset_form = AllAuthPasswordResetForm(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self):
        from allauth.account.forms import default_token_generator

        request = self.context.get("request")
        assert request is not None
        # Set some values to trigger the send_email method.
        opts = {
            "use_https": request.is_secure(),
            "from_email": getattr(
                settings, "DEFAULT_FROM_EMAIL", "noreply@{{cookiecutter.domain_name}}"
            ),
            "request": request,
            "token_generator": default_token_generator,
        }

        opts.update(self.get_email_options())
        assert self.reset_form is not None
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming a password reset attempt"""

    new_password = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    user = None
    set_password_form = None

    def validate(self, attrs):
        from allauth.account.forms import default_token_generator
        from allauth.account.utils import url_str_to_user_pk as uid_decoder

        # Decode the uidb64 (allauth use base36) to uid to get User object
        try:
            uid = force_str(uid_decoder(attrs["uid"]))
            self.user = User._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise exceptions.ValidationError({"uid": ["Invalid value"]})

        if not default_token_generator.check_token(self.user, attrs["token"]):
            raise exceptions.ValidationError({"token": ["Invalid value"]})

        # Construct SetPasswordForm instance
        attrs["new_password1"] = attrs["new_password"]
        attrs["new_password2"] = attrs["new_password"]

        self.set_password_form = SetPasswordForm(user=self.user, data=attrs)
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        assert self.set_password_form is not None
        return self.set_password_form.save()


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password = serializers.CharField(max_length=128)

    set_password_form = None

    def __init__(self, *args, **kwargs):
        self.logout_on_password_change = getattr(
            settings, "LOGOUT_ON_PASSWORD_CHANGE", False
        )
        super().__init__(*args, **kwargs)

        self.request = self.context.get("request")
        self.user = getattr(self.request, "user", None)

    def validate_old_password(self, value):

        if self.user and not self.user.check_password(value):
            err_msg = (
                "Your old password was entered incorrectly. Please enter it again."
            )
            raise serializers.ValidationError(err_msg)
        return value

    def validate(self, attrs):
        attrs = {
            "new_password1": attrs["new_password"],
            "new_password2": attrs["new_password"],
        }
        assert self.user is not None
        self.set_password_form = SetPasswordForm(user=self.user, data=attrs)

        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        assert self.set_password_form is not None
        self.set_password_form.save()
        if not self.logout_on_password_change:
            from django.contrib.auth import update_session_auth_hash

            assert self.request is not None
            assert self.user is not None
            update_session_auth_hash(self.request, self.user)
