"""
Module for all Form Tests.
"""
from ..forms import UserCreationForm
from ..models import User
from .factories import UserFactory


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
                "email": user.email,
                "password1": user.password,
                "password2": user.password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "email" in form.errors
        assert form.errors["email"][0] == "This email has already been taken."

    def test_password_validation_error_msg(self):
        """
        Tests UserAdminCreation Form's password validator functions correctly by testing:
            1) The passwords have to match.
            2) Only 1 error is raised by the UserCreation Form
            3) The desired error message is raised
        """

        # The passwords don't match, hence cannot be created.
        user = UserFactory.build()
        form = UserCreationForm(
            {
                "email": user.email,
                "password1": user.password,
                "password2": user.password + "2",
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "password2" in form.errors
        assert form.errors["password2"][0] == "Passwords don't match"

    def test_user_creation_with_commit(self):
        """
        Tests UserAdminCreation Form's save method by testing:
            1) The passwords have to match.
            2) No error is raised by the UserCreation Form
            3) The object is created during the test
        """

        # The passwords don't match, hence cannot be created.
        user = UserFactory.build()
        form = UserCreationForm(
            {
                "email": user.email,
                "password1": user.password,
                "password2": user.password,
            }
        )

        assert form.is_valid()
        form.save()

        assert len(form.errors) == 0
        assert len(User.objects.filter(email=user.email)) == 1
