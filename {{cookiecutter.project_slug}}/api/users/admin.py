from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from .forms import UserChangeForm
from .forms import UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        {%- if cookiecutter.username_type == "email" %}
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
        {%- else %}
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("name", "email")}),
        {%- endif %}
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["{{cookiecutter.username_type}}", "name", "is_superuser"]
    search_fields = ["name"]
    {%- if cookiecutter.username_type == "email" %}
    ordering = ["id"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    {%- endif %}
