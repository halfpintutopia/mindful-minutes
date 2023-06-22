from datetime import time

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import UserSettings

# retrieves the current active user model,
# which is set as the default user model AUTH_USER_MODEL, as extended AbstractUser
User = get_user_model()


class UserSettingsManagerTest(TestCase):
    """
    Test case for the user settings model
    """

    def setUp(self):
        """
        Set up the test environment for the UserSettings model tests

        This method is called before each test is run. It prepares the necessary data 
        and environment for the test case

        Steps:
        1. Create a user instance
        2. Create a UserSettings instance with the associated user and other attributes
        """
        # Create an instance of the User and UserSettings in memory rather than
        # using objects.create_user_settings() as this creates
        # and instance and save it to the database.
        self.user = User.objects.create_user(
            email="normal@user.com",
            password="abcdefghij123!+",
            first_name="Normal",
            last_name="User",
        )
        self.user_settings = UserSettings.objects.create_user_settings(
            user=self.user,
            start_week_day=1,
            morning_check_in=time(8, 30),
            evening_check_in=time(20, 30)
        )

    def test_create_user_settings(self):
        """
        GIVEN a user settings model
        WHEN creating the settings for the user
        THEN user should have the settings saved
        """

        self.assertEqual(self.user_settings.start_week_day,
                         1)
        self.assertEqual(self.user_settings.morning_check_in,
                         self.user_settings.morning_check_in)
        self.assertEqual(self.user_settings.evening_check_in,
                         self.user_settings.evening_check_in)
        self.assertIsInstance(self.user_settings.start_week_day, int)
        self.assertIsInstance(self.user_settings.morning_check_in, time)
        self.assertIsInstance(self.user_settings.evening_check_in, time)

    def test_create_user_settings_without_start_week_day(self):
        """
        GIVEN a user settings model
        WHEN creating the setting for the user without the start week day set
        THEN a ValueError should be raised
        """
        with self.assertRaises(TypeError):
            UserSettings.objects.create_user_settings(
                user=self.user,
                morning_check_in=self.user_settings.morning_check_in,
                evening_check_in=self.user_settings.evening_check_in
            )

    def test_create_user_settings_with_correct_start_week_day(self):
        """
        GIVEN a user settings model
        WHEN creating the settings for the user when the start week day is not an integer
        THEN a ValueError should be raised
        """
        with self.assertRaises(ValueError):
            UserSettings.objects.create_user_settings(
                user=self.user,
                start_week_day="string",
                morning_check_in=self.user_settings.morning_check_in,
                evening_check_in=self.user_settings.evening_check_in
            )

    def test_create_user_settings_without_morning_check_in(self):
        """
        GIVEN a user settings model
        WHEN creating the settings for the user when the morning check is missing
        THEN a ValueError should be raised
        """
        with self.assertRaises(TypeError):
            UserSettings.objects.create_user_settings(
                user=self.user,
                start_week_day=1,
                evening_check_in=self.user_settings.evening_check_in
            )

    def test_create_user_settings_with_incorrect_morning_check_in(self):
        """
        GIVEN a user settings model
        WHEN creating the settings for the user when the morning check in is not in time format
        THEN a ValueError should be raised
        """
        with self.assertRaises(ValueError):
            UserSettings.objects.create_user_settings(
                user=self.user,
                start_week_day=1,
                morning_check_in="random string",
                evening_check_in=self.user_settings.evening_check_in
            )

    def test_create_user_settings_without_evening_check_in(self):
        """
        GIVEN a user settings model
        WHEN creating the settings for the user when the evening check is missing
        THEN a TypeError should be raised
        """
        with self.assertRaises(TypeError):
            UserSettings.objects.create_user_settings(
                user=self.user,
                start_week_day=1,
                morning_check_in=self.user_settings.evening_check_in
            )

    def test_create_user_settings_with_incorrect_evening_check_in(self):
        """
        GIVEN a user settings model
        WHEN creating the settings for the user when the evening check in is not in time format
        THEN a ValueError should be raised
        """
        with self.assertRaises(ValueError):
            UserSettings.objects.create_user_settings(
                user=self.user,
                start_week_day=1,
                morning_check_in=self.user_settings.morning_check_in,
                evening_check_in="random string"
            )
