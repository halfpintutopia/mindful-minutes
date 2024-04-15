from datetime import time

import pytest

from user_settings.models import UserSettings


@pytest.mark.django_db
def test_create_user_settings(custom_user):
    """
    GIVEN a user settings model
    WHEN creating the settings for the user
    THEN user should have the settings saved
    """
    user_settings = UserSettings.objects.create(
        user=custom_user,
        start_week_day=1,
        morning_check_in=time(8, 30),
        evening_check_in=time(20, 30),
    )
    user_settings.save()
    user_settings_all = UserSettings.objects.all()
    assert len(user_settings_all) == 1
    assert user_settings_all[0].start_week_day == 1
    assert (
        isinstance(user_settings_all[0].start_week_day, int)
        and user_settings_all[0].start_week_day is not None
    )
    assert user_settings_all[0].morning_check_in == time(8, 30)
    assert (
        isinstance(user_settings_all[0].morning_check_in, time)
        and user_settings_all[0].morning_check_in is not None
    )
    assert user_settings_all[0].evening_check_in == time(20, 30)
    assert (
        isinstance(user_settings_all[0].evening_check_in, time)
        and user_settings_all[0].evening_check_in is not None
    )
    assert user_settings_all[0].user == custom_user
