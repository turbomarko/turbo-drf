{%- if cookiecutter.username_type == "email" %}from typing import ClassVar

{% endif -%}
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
{%- if cookiecutter.username_type == "email" %}
from django.db.models import EmailField
{%- endif %}
{%- if cookiecutter.username_type == "email" %}

from .managers import UserManager
{%- endif %}


class User(AbstractUser):
    """
    Default custom user model for {{cookiecutter.project_name}}.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField("Name of User", blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    {%- if cookiecutter.username_type == "email" %}
    email = EmailField("email address", unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()
    {%- endif %}

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        abstract = False
        db_table = "users"
