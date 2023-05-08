from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
{%- if cookiecutter.username_type == "email" %}
from django.forms import EmailField
{%- endif %}

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        {%- if cookiecutter.username_type == "email" %}
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": "This email has already been taken."},
        }
        {%- else %}
        error_messages = {
            "username": {"unique": "This username has already been taken."},
        }
        {%- endif %}


class UserChangeForm(forms.ModelForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        {%- if cookiecutter.username_type == "email" %}
        field_classes = {"email": EmailField}
        {%- endif %}
