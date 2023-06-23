import pytest

from django.contrib.auth import get_user_model

from journal.models import Target

User = get_user_model()


@pytest.fixture
def user():
    """
    Fixture for creating a user object
    """
    return User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User"
    )


@pytest.mark.django_db
def test_create_target(user):
    """
    GIVEN a target model
    WHEN creating a target
    THEN user should have successfully created a target
    """
    target = Target.objects.create(
        user=user,
        title="Meditate for 20 minutes",
        order=1,
    )
    target.save()
    targets = Target.objects.all()
    assert len(targets) == 1
    assert targets[0].user == user
    assert targets[0].title == "Meditate for 20 minutes"
    assert isinstance(targets[0].title, str) and targets[0].title is not None
    assert targets[0].order == 1
    assert isinstance(targets[0].order, int) and targets[0].order is not None
