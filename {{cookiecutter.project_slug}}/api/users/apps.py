import contextlib

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "api.users"
    verbose_name = "Users"

    def ready(self):
        with contextlib.suppress(ImportError):
            from . import signals # noqa: F401
