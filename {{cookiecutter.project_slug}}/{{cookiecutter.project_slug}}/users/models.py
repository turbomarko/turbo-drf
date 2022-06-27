import uuid

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

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and saves a superuser"""
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom UserModel that supports using email instead of username"""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="ID",
    )

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
