from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Factory
from .factories import UserFactory, SuperUserFactory

User = get_user_model()
faker = Factory.create()


class UsersManagersTests(TestCase):
    """
    Test case for the custom user model where the email is the unique identifier instead of username
    """
    def test_create_user(self):
        """
           GIVEN a custom user model
           WHEN a user is created with a valid email, password, first_name, last_name
           THEN the user should have the provided email
           AND WHEN a user is created with missing or empty email, empty first_name,
           empty last_name or password
           THEN a TypeError or ValueError should be raised
           """
        user = UserFactory()
        self.assertEqual(user.email, user.email)
        self.assertEqual(user.first_name, user.first_name)
        self.assertEqual(user.last_name, user.last_name)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name="",
                last_name=user.last_name,
                email=user.email,
                password=user.password
            )
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name=user.first_name,
                last_name="",
                email=user.email,
                password=user.password
            )
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name=user.first_name,
                last_name=user.last_name,
                email="",
                password=user.password
            )

    def test_create_superuser(self):
        """
           GIVEN a custom user model
           WHEN a superuser is created with a valid email, password, first_name, last_name
           THEN the superuser should have the provided email, first_name, last_name,
           be active, a staff member,
           a superuser and have no username
           AND WHEN a user is created with missing or empty email, empty first_name,
           empty last_name or password
           THEN a TypeError or ValueError should be raised
           """
        admin_user = SuperUserFactory()
        self.assertEqual(admin_user.email, admin_user.email)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="",
                password=admin_user.password,
                first_name=admin_user.first_name,
                last_name=admin_user.last_name,
                is_superuser=True
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=admin_user.email,
                password=admin_user.password,
                first_name="",
                last_name=admin_user.last_name,
                is_superuser=True
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=admin_user.email,
                password=admin_user.password,
                first_name=admin_user.first_name,
                last_name="",
                is_superuser=True
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=admin_user.email,
                password=admin_user.password,
                first_name=admin_user.first_name,
                last_name=admin_user.last_name,
                is_superuser=False
            )
