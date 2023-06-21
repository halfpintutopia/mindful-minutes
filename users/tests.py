from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Factory
# from .factories.users import UserFactory, SuperUserFactory

User = get_user_model()
# faker = Factory.create()


class UsersManagersTests(TestCase):
    """
    Test case for the custom user model where the email is the unique identifier instead of username
    """

    def setUp(self):
        self.user = User.objects.create_user(
            email="normal@user.com",
            password="abcdefghij123456!+",
            first_name="Normal First Name",
            last_name="Normal Last Name",
        )
        self.admin_user = User.objects.create_superuser(
            email="super@user.com",
            password="abcdefghij123456!+",
            first_name="Super First Name",
            last_name="Super Last Name",
            is_active=True,
            is_staff=True,
            is_superuser=True
        )

    def test_create_user(self):
        """
           GIVEN a custom user model
           WHEN a user is created with a valid email, password, first_name, last_name
           THEN the user should have the provided email saved
           """
        # user = User.objects.create_user(
        #     email="normal@user.com",
        #     password="abcdefghij123456!+",
        #     first_name="Normal First Name"
        #     last_name="Normal Last Name",
        # )
        self.assertEqual(self.user.email, "normal@user.com")
        self.assertEqual(self.user.first_name, "Normal First Name")
        self.assertEqual(self.user.last_name, "Normal Last Name")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        try:
            self.assertIsNone(self.user.username)
        except AttributeError:
            pass

    def test_create_user_with_no_data(self):
        """
        GIVEN a custom user model
        WHEN a user is created with no email, password, first_name, last_name
        THEN a TypeError is raised
        """
        with self.assertRaises(TypeError):
            User.objects.create_user()

    def test_create_user_an_empty_string_for_email(self):
        """
        GIVEN a custom user model
        WHEN a user is created with an empty string for the email
        THEN a TypeError should be raised
        """
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")

    def test_create_user_without_first_name(self):
        """
        GIVEN a custom user model
        WHEN a user is created with an empty string for the first_name
        THEN a ValueError is raised
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name="",
                last_name=self.user.last_name,
                email=self.user.email,
                password=self.user.password
            )

    def test_create_user_without_last_name(self):
        """
        GIVEN a custom user model
        WHEN a user is created with an empty string for the last_name
        THEN a ValueError is raised
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name=self.user.first_name,
                last_name="",
                email=self.user.email,
                password=self.user.password
            )

    def test_create_user_without_password(self):
        """
        GIVEN a custom user model
        WHEN a user is created with an empty string for a the password
        THEN a ValueError is raised
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name=self.user.first_name,
                last_name=self.user.last_name,
                email="normal1@user.com",
                password=""
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
        # admin_user = User.objects.create_superuser(
        #     email="super@user.com",
        #     password="abcdefghij123456!+",
        #     first_name="Normal First Name",
        #     last_name="Normal Last Name",
        # )
        self.assertEqual(self.admin_user.email, self.admin_user.email)
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)
        try:
            self.assertIsNone(self.admin_user.username)
        except AttributeError:
            pass

    def test_create_superuser_without_data(self):
        """
        GIVEN a custom user model
        WHEN a super user is created without data
        THEN a TypeError should be raised
        """
        with self.assertRaises(TypeError):
            User.objects.create_superuser()

    def test_create_superuser_without_email(self):
        """
        GIVEN a custom model
        WHEN a super user is created without an email
        THEN a ValueError should be raised
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="",
                password=self.admin_user.password,
                first_name=self.admin_user.first_name,
                last_name=self.admin_user.last_name,
                is_active=True,
                is_staff=True,
                is_superuser=True
            )

    def test_create_superuser_without_first_name(self):
        """
        GIVEN a custom user model
        WHEN a super user is created without first name
        THEN a ValueError should be raised
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.admin_user.email,
                password=self.admin_user.password,
                first_name="",
                last_name=self.admin_user.last_name,
                is_active=True,
                is_staff=True,
                is_superuser=True
            )

    def test_create_superuser_without_last_name(self):
        """
        GIVEN a custom user model
        WHEN a super user is created without a last name
        THEN a ValueError should be raised
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.admin_user.email,
                password=self.admin_user.password,
                first_name=self.admin_user.first_name,
                last_name="",
                is_active=True,
                is_staff=True,
                is_superuser=True
            )

    def test_create_superuser_when_not_active(self):
        """
        GIVEN a custom user model
        WHEN a super user is created when not active
        THEN a ValueError should be raised
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super1@user.com",
                password=self.admin_user.password,
                first_name=self.admin_user.first_name,
                last_name=self.admin_user.last_name,
                is_active=False,
                is_staff=True,
                is_superuser=True
            )

    def test_create_superuser_when_not_staff(self):
        """
        GIVEN a custom user model
        WHEN a super user is created when not staff
        THEN a ValueError should be raised
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.admin_user.email,
                password=self.admin_user.password,
                first_name=self.admin_user.first_name,
                last_name=self.admin_user.last_name,
                is_active=True,
                is_staff=False,
                is_superuser=True
            )

    def test_create_superuser_when_not_superuser(self):
        """
        GIVEN a custom user model
        WHEN a super user is created when not a super user
        THEN a ValueError should be raised
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.admin_user.email,
                password=self.admin_user.password,
                first_name=self.admin_user.first_name,
                last_name=self.admin_user.last_name,
                is_active=True,
                is_staff=True,
                is_superuser=False
            )
