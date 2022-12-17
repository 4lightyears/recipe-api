"""
Manager class for the user.
"""

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Manager for User."""

    def create_user(self, email, password=None, **other_fields):
        """Creates the user"""

        if not email:
            raise ValueError('Email is required! User must have an email.')
        user = self.model(email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates a new super user and returns it."""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
