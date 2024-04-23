from allauth.account.utils import has_verified_email
from rest_framework.permissions import SAFE_METHODS
from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # We'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user


class IsEmailVerified(BasePermission):
    """
    Object-level permission to only allow users with verified emails to access the view.
    """

    def has_object_permission(self, request, view, obj):
        return has_verified_email(request.user)
