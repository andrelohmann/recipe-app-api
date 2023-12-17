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
        name = 'Test user'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            name=name,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        password = 'test_p@ss.123!'
        name = 'Test user'
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.Com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email,
                password,
                name=name,
            )
            self.assertEqual(user.email, expected)

    def test_user_email_is_unique(self):
        """Test user email is unique."""
        email = 'test1@example.com'
        passw = 'sample123'
        name = 'Test user'
        user = get_user_model().objects.create_user(
            email,
            passw,
            name=name,
        )

        with self.assertRaises(IntegrityError):
            user = get_user_model().objects.create_user(
                email,
                passw,
                name=name,
            )
            self.assertEqual(user.email, email)

    def test_new_user_without_name_raises_error(self):
        """Test that creating a user without a name raises a ValueError."""
        email = 'test1@example.com'
        passw = 'sample123'
        name = ''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email, passw)

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email,
                passw,
                name=name,
            )

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        email = ''
        passw = 'sample123'
        name = 'Test user'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email,
                passw,
                name=name,
            )

    def test_create_superuser(self):
        """Test creating a superuser."""
        email = 'test1@example.com'
        passw = 'sample123'
        name = 'Test user'
        user = get_user_model().objects.create_superuser(
            email,
            passw,
            name=name,
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_with_default_name(self):
        """
        Test creating a superuser without a name to be given
        the default namen 'Superuser'.
        """
        email = 'test1@example.com'
        passw = 'sample123'
        user = get_user_model().objects.create_superuser(
            email,
            passw,
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEquals(user.name, 'Superuser')
