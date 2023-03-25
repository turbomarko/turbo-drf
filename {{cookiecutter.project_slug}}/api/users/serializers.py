from dj_rest_auth.registration.serializers import (
    RegisterSerializer as BaseRegisterSerializer,
)
from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "is_staff"]
        read_only_fields = ("is_staff",)

    def validate_email(self, value):
        """Make the email lowercase"""
        return value.lower()


class LoginSerializer(BaseLoginSerializer):
    username = None


class RegisterSerializer(BaseRegisterSerializer):
    username = None
