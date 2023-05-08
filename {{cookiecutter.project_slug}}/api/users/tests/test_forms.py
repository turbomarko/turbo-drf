"""
Module for all Form Tests.
"""
import pytest

from ..forms import UserCreationForm
from ..models import User
from .factories import UserFactory


@pytest.mark.django_db
class TestUserAdminCreationForm:
    """
    Test class for all tests related to the UserCreationForm
    """

    def test_email_duplication_error_msg(self, user: User):
        """
        Tests UserAdminCreation Form's unique validator functions correctly by testing:
            1) A new user with an existing email cannot be added.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """

        # The user already exists,
        # hence cannot be created.
        form = UserCreationForm(
            {
                {%- if cookiecutter.username_type == "email" %}
                "email": user.email,
                {%- else %}
                "username": user.username,
                {%- endif %}
                "password1": user.password,
                "password2": user.password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        {%- if cookiecutter.username_type == "email" %}
        assert "email" in form.errors
        assert form.errors["email"][0] == "This email has already been taken."
        {%- else %}
        assert "username" in form.errors
        assert form.errors["username"][0] == "This username has already been taken."
        {%- endif %}
