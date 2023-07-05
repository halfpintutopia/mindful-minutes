import pytest

from django.contrib.auth import get_user_model

from faker import Faker

User = get_user_model()
fake = Faker()


@pytest.mark.django_db
def test_create_custom_user():
    """
    GIVEN a User model
    WHEN a new user is created
    THEN check the email, password, first_name, last_name
    """
    email = fake.email()
    password = fake.password()
    first_name = fake.first_name()
    last_name = fake.last_name()

    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )

    assert user.email == email
    assert user.check_password(password)
    assert user.first_name == first_name
    assert user.last_name == last_name
