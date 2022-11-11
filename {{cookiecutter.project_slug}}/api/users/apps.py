from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "api.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import api.users.signals  # noqa F401
        except ImportError:
            pass
