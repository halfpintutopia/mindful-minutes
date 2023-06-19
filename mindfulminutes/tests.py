from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    def test_create_user(self):
        """
           GIVEN a custom user model
           WHEN a user is created with a valid email, password, first_name, last_name
           THEN the user should have the provided email
           AND WHEN a user is created with missing or empty email, empty first_name, empty last_name or password
           THEN a TypeError or ValueError should be raised
           """
        User = get_user_model()
        user = User.objects.create_user(
            email="samsmith@user.com",
            password="thecorrectlength123",
            first_name="Sam",
            last_name="Smith"
            )
        self.assertEqual(user.email, "samsmith@user.com")
        self.assertEqual(user.first_name, "Sam")
        self.assertEqual(user.last_name, "Smith")
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
                last_name="Smith",
                email="thecorrectlength123"
                )
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name="Sam",
                last_name="",
                email="thecorrectlength123"
                )
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name="Sam",
                email="",
                password="thecorrectlength123"
                )

    def test_create_superuser(self):
        """
           GIVEN a custom user model
           WHEN a superuser is created with a valid email, password, first_name, last_name
           THEN the superuser should have the provided email, first_name, last_name, be active, a staff member,
           a superuser and have no username
           AND WHEN a user is created with missing or empty email, empty first_name, empty last_name or password
           THEN a TypeError or ValueError should be raised
           """
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="adminsamsmith@user.com",
            password="admincorrectlength123",
            first_name="Sam",
            last_name="Smith"
            )
        self.assertEqual(admin_user.email, "adminsamsmith@user.com")
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
                password="admincorrectlength123",
                first_name="Sam",
                last_name="Smith",
                is_superuser=True
                )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="adminsamsmith@user.com",
                password="admincorrectlength123",
                first_name="",
                last_name="Smith",
                is_superuser=True
                )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="adminsamsmith@user.com",
                password="admincorrectlength123",
                first_name="Sam",
                last_name="",
                is_superuser=True
                )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="adminsamsmith@user.com",
                password="admincorrectlength123",
                first_name="Sam",
                last_name="Smith",
                is_superuser=False
                )


