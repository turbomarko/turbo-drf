from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and save new user"""
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=email.lower(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and saves a superuser"""
        user = self.create_user(email.lower(), password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model that supports using email for login instead of username"""

    # Modifiable fields
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(
        default=True, help_text="Only active users can authenticate."
    )
    is_admin = models.BooleanField(
        default=False, help_text="Users with admin rights can access the admin page."
    )

    # Automatic fields
    date_joined = models.DateTimeField(auto_now_add=True)

    # Data cleanup
    def clean(self):
        super().clean()
        self.email = self.email.lower()

    # Read-only properties
    @property
    def is_staff(self):
        # All admins are staff
        return self.is_admin

    # Dunder methods
    def __str__(self):
        return self.email

    # Extra variables
    USERNAME_FIELD = "email"
    objects = UserManager()
