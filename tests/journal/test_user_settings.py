from datetime import time

import pytest

from django.contrib.auth import get_user_model

from journal.models import UserSettings

# retrieves the current active user model,
# which is set as the default user model AUTH_USER_MODEL,
# as extended AbstractUser
User = get_user_model()


@pytest.fixture
def user():
    """
    Fixture for creating a user object.
    """
    return User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )


@pytest.mark.django_db
def test_create_user_settings(user):
    """
    GIVEN a user settings model
    WHEN creating the settings for the user
    THEN user should have the settings saved
    """
    user_settings = UserSettings.objects.create(
        user=user,
        start_week_day=1,
        morning_check_in=time(8, 30),
        evening_check_in=time(20, 30)
    )
    user_settings.save()
    user_settings_all = UserSettings.objects.all()
    assert len(user_settings_all) == 1
    assert user_settings_all[0].start_week_day == 1
    assert isinstance(
        user_settings_all[0].start_week_day, int
    ) and user_settings_all[0].start_week_day is not None
    assert user_settings_all[0].morning_check_in == time(8, 30)
    assert isinstance(
        user_settings_all[0].morning_check_in, time
    ) and user_settings_all[0].morning_check_in is not None
    assert user_settings_all[0].evening_check_in == time(20, 30)
    assert isinstance(
        user_settings_all[0].evening_check_in, time
    ) and user_settings_all[0].evening_check_in is not None
    assert user_settings_all[0].user == user
