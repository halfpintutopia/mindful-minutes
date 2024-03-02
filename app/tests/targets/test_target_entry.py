import pytest

from targets.models import TargetEntry


@pytest.mark.django_db
def test_create_target(custom_user):
    """
    GIVEN a target model
    WHEN creating a target
    THEN user should have successfully created a target
    """
    target = TargetEntry.objects.create(
        user=custom_user,
        title="Meditate for 20 minutes",
        order=1,
    )
    target.save()
    targets = TargetEntry.objects.all()
    assert len(targets) == 1
    assert targets[0].user == custom_user
    assert targets[0].title == "Meditate for 20 minutes"
    assert isinstance(targets[0].title, str) and targets[0].title is not None
    assert targets[0].order == 1
    assert isinstance(targets[0].order, int) and targets[0].order is not None
