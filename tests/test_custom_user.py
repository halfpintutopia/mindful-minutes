import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    """
    GIVEN a CustomUser model
    WHEN a new user is created
    THEN the user is successfully created with the provided data
    """
    first_name = 'Sirinya'
    last_name = 'Richardson'
    email = 'siri@notanemail.com'
    password = 'password'

    user = User.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        is_superuser=False,
        is_staff=False,
        is_active=True
    )

    assert user.email == email
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.check_password(password)
    assert not user.is_staff
    assert user.is_active
    assert not user.is_superuser
    assert not user.is_staff
