from datetime import date, time

import pytest

from journal.serializers import CustomUserSerializer
from journal.models import UserSettings


@pytest.mark.django_db
def test_custom_user_serializer(custom_user):
    """
    GIVEN a valid custom user serializer
    WHEN the data is passed to th serializer
    THEN the serializer should be valid
    """
    start_week_day = 1
    morning_check_in = time(9, 0)
    evening_check_in = time(17, 0)

    UserSettings.objects.create(
        user=custom_user,
        start_week_day=start_week_day,
        morning_check_in=morning_check_in,
        evening_check_in=evening_check_in
    )

    serializer = CustomUserSerializer(custom_user)

    assert serializer.data.get("is_active") is True

    # Verify the serializer raises Attribute error when encountering unrecognised fields (keys)
    # with pytest.raises(AttributeError):
    #     CustomUserSerializer(data={**serializer.data, "dark_mode": False})

    assert serializer.data.get("user_settings", {}).get(
        "start_week_day") == start_week_day
    assert serializer.data.get("user_settings", {}).get(
        "morning_check_in") == morning_check_in.strftime("%H:%M:%S")
    assert serializer.data.get("user_settings", {}).get(
        "evening_check_in") == evening_check_in.strftime("%H:%M:%S")
    assert serializer.data.get("user_settings", {}).get(
        "user") == custom_user.id
