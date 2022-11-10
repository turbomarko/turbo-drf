from allauth.account import app_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.utils import import_attribute
from django.conf import settings


class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        frontend_url = getattr(settings, "FRONTEND_URL", "")
        url = frontend_url + "confirm-email/" + emailconfirmation.key
        return url


def get_adapter(request=None):
    """
    The Adapter in app_settings.ADAPTER is set to CustomAccountAdapter.
    """
    return import_attribute(app_settings.ADAPTER)(request)
