import contextlib

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "api.users"
    verbose_name = "Users"

    def ready(self):
        with contextlib.suppress(ImportError):
            import api.users.signals  # noqa: F401
