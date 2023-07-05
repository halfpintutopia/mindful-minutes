from datetime import date, time

import pytest

from faker import Faker

from django.contrib.auth import get_user_model

from journal.serializers import CustomUserSerializer
from journal.models import UserSettings

User = get_user_model()
fake = Faker()


@pytest.mark.django_db
def test_custom_user_serializer():
    """
    GIVEN a valid custom user serializer
    WHEN the data is passed to th serializer
    THEN the serializer should be valid
    """
    email = fake.email()
    password = fake.password(length=16)
    first_name = fake.first_name()
    last_name = fake.last_name()

    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    start_week_day = 1
    morning_check_in = time(9, 0)
    evening_check_in = time(17, 0)

    UserSettings.objects.create(
        user=user,
        start_week_day=start_week_day,
        morning_check_in=morning_check_in,
        evening_check_in=evening_check_in
    )

    serializer = CustomUserSerializer(user)

    assert serializer.data.get("is_active") is True

    # Verify the serializer raises Attribute error when encountering unrecognised fields (keys)
    # with pytest.raises(AttributeError):
    #     CustomUserSerializer(data={**serializer.data, "dark_mode": False})

    assert serializer.data.get("user_settings", {}).get("start_week_day") == start_week_day
    assert serializer.data.get("user_settings", {}).get(
        "morning_check_in") == morning_check_in.strftime("%H:%M:%S")
    assert serializer.data.get("user_settings", {}).get(
        "evening_check_in") == evening_check_in.strftime("%H:%M:%S")
    assert serializer.data.get("user_settings", {}).get("user") == user.id
