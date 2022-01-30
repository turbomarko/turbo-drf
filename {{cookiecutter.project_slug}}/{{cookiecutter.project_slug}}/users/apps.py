from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "{{ cookiecutter.project_slug }}.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import {{ cookiecutter.project_slug }}.users.signals  # noqa F401
        except ImportError:
            pass
