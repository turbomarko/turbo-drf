from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from api.utils.permissions import IsEmailVerified
from api.utils.permissions import IsOwnerOrReadOnly

User = get_user_model()
factory = APIRequestFactory()


# Test IsOwnerOrReadOnly Permission
@pytest.mark.django_db
class TestIsOwnerOrReadOnly:
    def test_allows_safe_methods(self):
        """
        Tests that safe methods are allowed regardless of ownership.
        """
        permission = IsOwnerOrReadOnly()
        owner = User.objects.create(email="owner@test.com")
        other_user = User.objects.create(email="other_user@test.com")
        request = factory.get("/")  # Safe method

        # Create a mock object with an `owner` attribute
        obj = type("TestObject", (object,), {"owner": owner})

        # Test as owner and non-owner
        request.user = owner
        assert permission.has_object_permission(request, None, obj) is True

        request.user = other_user
        assert permission.has_object_permission(request, None, obj) is True

    def test_denies_non_safe_methods_for_non_owner(self):
        """
        Tests that non-safe methods are denied for non-owners.
        """
        permission = IsOwnerOrReadOnly()
        owner = User.objects.create(email="owner@test.com")
        other_user = User.objects.create(email="other_user@test.com")
        request = factory.post("/")  # Non-safe method

        # Create a mock object with an `owner` attribute
        obj = type("TestObject", (object,), {"owner": owner})

        request.user = other_user
        assert permission.has_object_permission(request, None, obj) is False

    def test_allows_non_safe_methods_for_owner(self):
        """
        Tests that non-safe methods are allowed for the owner.
        """
        permission = IsOwnerOrReadOnly()
        owner = User.objects.create(email="owner@test.com")
        request = factory.post("/")  # Non-safe method

        # Create a mock object with an `owner` attribute
        obj = type("TestObject", (object,), {"owner": owner})

        request.user = owner
        assert permission.has_object_permission(request, None, obj) is True


# Test IsEmailVerified Permission
@pytest.mark.django_db
class TestIsEmailVerified:
    @patch("allauth.account.utils.has_verified_email")
    def test_denies_access_for_unverified_email(self, mock_has_verified_email):
        """
        Tests that access is denied if the user's email is not verified.
        """
        mock_has_verified_email.return_value = False
        permission = IsEmailVerified()
        user = User.objects.create(email="unverified_user@test.com")
        request = factory.get("/")
        request.user = user

        assert permission.has_object_permission(request, None, None) is False
