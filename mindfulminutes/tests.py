from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UsersManagersTests(TestCase):
    """
    Test case for the custom user model where the email is the unique identifier instead of username
    """

    def setUp(self):
        self.email = "another@user.com"
        self.password = "thecorrectlength123"
        self.first_name = "Sam"
        self.last_name = "Smith"

    def test_create_user(self):
        """
           GIVEN a custom user model
           WHEN a user is created with a valid email, password, first_name, last_name
           THEN the user should have the provided email
           AND WHEN a user is created with missing or empty email, empty first_name,
           empty last_name or password
           THEN a TypeError or ValueError should be raised
           """
        user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name
        )
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
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
                last_name=self.last_name,
                email="unique1@user.com",
                password=self.password
            )
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name=self.first_name,
                last_name="",
                email="unique2@user.com",
                password=self.password
            )
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name=self.first_name,
                last_name=self.last_name,
                email="",
                password=self.password
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
        admin_user = User.objects.create_superuser(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name
        )
        self.assertEqual(admin_user.email, self.email)
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
                password=self.password,
                first_name=self.first_name,
                last_name=self.last_name,
                is_superuser=True
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="unique3@user.com",
                password=self.password,
                first_name="",
                last_name=self.last_name,
                is_superuser=True
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="unique4@user.com",
                password=self.password,
                first_name=self.first_name,
                last_name="",
                is_superuser=True
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="unique5@user.com",
                password=self.password,
                first_name=self.first_name,
                last_name=self.last_name,
                is_superuser=False
            )
