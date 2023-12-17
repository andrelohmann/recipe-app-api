"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successfull."""
        email = 'test@example.com'
        password = 'test_p@ss.123!'
        first_name = 'Test'
        last_name = 'User'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        password = 'test_p@ss.123!'
        first_name = 'Test'
        last_name = 'User'
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.Com', 'test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'test3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email,
                password,
                first_name=first_name,
                last_name=last_name,
            )
            self.assertEqual(user.email, expected)

    def test_user_email_is_unique(self):
        """Test user email is unique."""
        email = 'test1@example.com'
        passw = 'sample123'
        first_name = 'Test'
        last_name = 'User'
        user = get_user_model().objects.create_user(
            email,
            passw,
            first_name=first_name,
            last_name=last_name,
        )

        with self.assertRaises(IntegrityError):
            user = get_user_model().objects.create_user(
                email,
                passw,
                first_name=first_name,
                last_name=last_name,
            )
            self.assertEqual(user.email, email)

    def test_new_user_without_first_name_raises_error(self):
        """Test that creating a user without a name raises a ValueError."""
        email = 'test1@example.com'
        passw = 'sample123'
        first_name = ''
        last_name = 'User'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email, passw)

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email,
                passw,
                first_name=first_name,
                last_name=last_name,
            )

    def test_new_user_without_last_name_raises_error(self):
        """Test that creating a user without a name raises a ValueError."""
        email = 'test1@example.com'
        passw = 'sample123'
        first_name = 'Test'
        last_name = ''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email, passw)

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email,
                passw,
                first_name=first_name,
                last_name=last_name,
            )

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        email = ''
        passw = 'sample123'
        first_name = 'Test'
        last_name = 'User'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email,
                passw,
                first_name=first_name,
                last_name=last_name,
            )

    def test_create_superuser(self):
        """Test creating a superuser."""
        email = 'test1@example.com'
        passw = 'sample123'
        first_name = 'Super'
        last_name = 'User'
        user = get_user_model().objects.create_superuser(
            email,
            passw,
            first_name=first_name,
            last_name=last_name,
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)