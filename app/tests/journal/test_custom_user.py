import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_custom_user_model():
    """
    GIVEN a custom user model
    WHEN a user is created with a valid email, password, first_name, last_name
    THEN the user should have the provided email saved
    """
    user = User.objects.create_user(
        email="normal@user.com",
        password="abcdefghij123!+_",
        first_name="Normal",
        last_name="User",
    )
    user.save()
    assert user.email == "normal@user.com"
    assert user.first_name == "Normal"
    assert user.last_name == "User"
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.username is None
    assert user.unique_identifier is not None
    assert user.slug == f"normal-user-{user.unique_identifier}"


@pytest.mark.django_db
def test_create_user_with_no_data():
    """
    GIVEN a custom user model
    WHEN a user is created with no email, password, first_name, last_name
    THEN a TypeError is raised
    """
    with pytest.raises(TypeError):
        User.objects.create_user()


@pytest.mark.django_db
def test_create_user_an_empty_string_for_email():
    """
    GIVEN a custom user model
    WHEN a user is created with an empty string for the email
    THEN a TypeError should be raised
    """
    with pytest.raises(TypeError):
        User.objects.create_user(email="")


@pytest.mark.django_db
def test_create_user_without_first_name():
    """
    GIVEN a custom user model
    WHEN a user is created with an empty string for the first_name
    THEN a ValueError is raised
    """
    with pytest.raises(ValueError):
        User.objects.create_user(
            email="normal@user.com",
            password="abcdefghij123!+_",
            first_name="",
            last_name="User",
        )


@pytest.mark.django_db
def test_create_user_without_last_name():
    """
    GIVEN a custom user model
    WHEN a user is created with an empty string for the last_name
    THEN a ValueError is raised
    """
    with pytest.raises(ValueError):
        User.objects.create_user(
            email="normal@user.com",
            password="abcdefghij123!+_",
            first_name="Normal",
            last_name="",
        )


@pytest.mark.django_db
def test_create_user_without_password():
    """
    GIVEN a custom user model
    WHEN a user is created with an empty string for a the password
    THEN a ValueError is raised
    """
    with pytest.raises(ValueError):
        User.objects.create_user(
            email="normal@user.com", password="", first_name="Normal", last_name="User"
        )


@pytest.mark.django_db
def test_create_superuser():
    """
    GIVEN a custom user model
    WHEN a superuser is created with
    a valid email, password, first_name, last_name
    THEN the superuser should have
    the provided email, first_name, last_name,
    be active, a staff member
    """
    admin_user = User.objects.create_superuser(
        email="super@user.com",
        password="abcdefghij123456!+",
        first_name="Super First Name",
        last_name="Super Last Name",
    )
    assert admin_user.email == "super@user.com"
    assert admin_user.first_name == "Super First Name"
    assert admin_user.last_name == "Super Last Name"
    assert admin_user.is_active is True
    assert admin_user.is_staff is True
    assert admin_user.is_superuser is True
    assert admin_user.username is None


@pytest.mark.django_db
def test_create_superuser_without_data():
    """
    GIVEN a custom user model
    WHEN a super user is created without data
    THEN a TypeError should be raised
    """
    with pytest.raises(TypeError):
        User.objects.create_superuser()


@pytest.mark.django_db
def test_create_superuser_without_email():
    """
    GIVEN a custom model
    WHEN a super user is created without an email
    THEN a ValueError should be raised
    """
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="",
            password="abcdefghij123456!+",
            first_name="Super First Name",
            last_name="Super Last Name",
        )


@pytest.mark.django_db
def test_create_superuser_without_first_name():
    """
    GIVEN a custom user model
    WHEN a super user is created without first name
    THEN a ValueError should be raised
    """
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="super@user.com",
            password="abcdefghij123456!+",
            first_name="",
            last_name="Super Last Name",
        )


@pytest.mark.django_db
def test_create_superuser_without_last_name():
    """
    GIVEN a custom user model
    WHEN a super user is created without a last name
    THEN a ValueError should be raised
    """
    with pytest.raises(ValueError):
        User.objects.create_superuser(
            email="super@user.com",
            password="abcdefghij123456!+",
            first_name="Super First Name",
            last_name="",
        )
