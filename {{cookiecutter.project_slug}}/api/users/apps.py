from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "api.users"
    verbose_name = "Users"

    def ready(self):
        try:
            from . import signals  # type: ignore # noqa: F401
        except ImportError:
            pass
