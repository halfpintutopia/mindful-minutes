from datetime import time

import pytest

from faker import Faker

from django.contrib.auth import get_user_model

from journal.models import UserSettings


User = get_user_model()
fake = Faker()


@pytest.mark.django_db
def test_create_user_settings():
    """
    GIVEN a UserSettings model
    WHEN a new user settings are created
    THEN check the user, start_week_day,
    morning_check_in, evening_check_in
    """
    user = User.objects.create_user(
        email=fake.email(),
        password=fake.password(length=16),
        first_name=fake.first_name(),
        last_name=fake.last_name()
    )
    start_week_day = 1
    morning_check_in = time(9, 0)
    evening_check_in = time(17, 0)

    user_settings = UserSettings.objects.create(
        user=user,
        start_week_day=start_week_day,
        morning_check_in=morning_check_in,
        evening_check_in=evening_check_in
    )

    assert user_settings.user == user
    assert user_settings.start_week_day == start_week_day
    assert user_settings.morning_check_in == morning_check_in
    assert user_settings.evening_check_in == evening_check_in
    assert user_settings.created_on is not None
    assert user_settings.updated_on is not None
