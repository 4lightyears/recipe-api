"""
Contains unit tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    """Tests the user model."""

    def test_create_with_email_successful(self):
        """Check if the user was successfully created with email."""

        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email_new_user(self):
        """Test if the email is normalized for the new user."""

        sample_emails = [
            ['test1@EXAMPLE.COM', 'test1@example.com'],
            ['test2@Example.com', 'test2@example.com'],
            ['Test@Example.com', 'Test@example.com'],
            ['test@example.com', 'test@example.com'],
        ]

        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(
                email=email, password='sample123'
            )
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """Test that a new user when being created without an email raises ValueError"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test1234')

    def test_create_superuser(self):
        """Test the creation of a superuser."""

        user = get_user_model().objects.create_superuser(
            'test1@example.com', 'test1234'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
