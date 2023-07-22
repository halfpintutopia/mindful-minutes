import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status

User = get_user_model()
fake = Faker()


@pytest.mark.django_db
def test_list_all_custom_users(authenticated_user, add_custom_user):
    """
    GIVEN a Django application
    WHEN the user requests all the appointment entries
    THEN the user should receive a list of all the appointment entries
    """
    (client, *_) = authenticated_user

    for num in range(4):
        add_custom_user(
            email=fake.email(),
            password=fake.password(length=16),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )

    url = reverse("user-list")

    res = client.get(url, content_type="application/json")

    assert res.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_add_custom_user(client):
    """
    GIVEN a Django application
    WHEN the user creates a new account
    THEN a new user is created
    """
    users = User.objects.all()
    assert len(users) == 0

    email = fake.email()
    password = fake.password()
    first_name = fake.first_name()
    last_name = fake.last_name()

    data = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
    }

    url = reverse("user-list")

    res = client.post(url, data, content_type="application/json")

    assert res.status_code == status.HTTP_201_CREATED
    assert res.data["email"] == email
    assert res.data["first_name"] == first_name
    assert res.data["last_name"] == last_name

    users = User.objects.all()
    assert len(users) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {
            "payload": {
                "email": fake.email(),
                "password": fake.password(length=16),
                "first_name": fake.first_name(),
            }
        },
        {
            "payload": {
                "email": fake.email(),
                "password": fake.password(length=16),
                "first name": fake.first_name(),
            }
        },
        {
            "payload": {
                "email": fake.email(),
                "password": fake.password(length=16),
                "last_name": fake.last_name(),
            }
        },
        {
            "payload": {
                "email": fake.email(),
                "password": fake.password(length=16),
                "last name": fake.last_name(),
            }
        },
        {
            "payload": {
                "email": fake.email(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            }
        },
        {
            "payload": {
                "email": fake.email(),
                "first name": fake.first_name(),
                "last name": fake.last_name(),
            }
        },
        {
            "payload": {
                "password": fake.password(length=16),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            }
        },
        {
            "payload": {
                "password": fake.password(length=16),
                "first name": fake.first_name(),
                "last name": fake.last_name(),
            }
        },
        {"payload": {}},
    ],
)
def test_add_custom_user_invalid_data(client, test_data):
    """
    GIVEN a Django application
    WHEN the user creates a new account with invalid data
    THEN a new user is not created
    """
    url = reverse("user-list")

    payload = {
        "email": fake.email(),
        "password": fake.password(length=16),
        "first_name": fake.first_name(),
    }

    res = client.post(url, payload, content_type="application/json")

    assert res.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_custom_user(client, add_custom_user):
    """
    GIVEN a Django application
    WHEN the user requests a user
    THEN
    """
    email = fake.email()
    password = fake.password(length=16)
    first_name = fake.first_name()
    last_name = fake.last_name()

    user = add_custom_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    url = reverse("user-detail", args=[user.slug])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK
    assert res.data["email"] == email
    assert res.data["first_name"] == first_name
    assert res.data["last_name"] == last_name


@pytest.mark.django_db
def test_get_custom_user_incorrect_id(client):
    """
    GIVEN a Django application
    WHEN the user requests a user with an incorrect id
    THEN the user is not found, a 404 is returned
    """
    invalid_id = 1245
    url = reverse("user-detail", args=[invalid_id])

    res = client.get(url)

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_all_users(client, add_custom_user):
    """
    GIVEN a Django application
    WHEN the user requests all users
    THEN the list of users is returned
    """
    users = User.objects.all()
    assert len(users) == 0

    for num in range(3):
        email = fake.email()
        password = fake.password(length=16)
        first_name = fake.first_name()
        last_name = fake.last_name()

        add_custom_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

    url = reverse("user-list")

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK

    users = User.objects.all()
    assert len(users) == 3


@pytest.mark.django_db
def test_remove_custom_user(client, add_custom_user):
    """
    GIVEN a Django application
    WHEN the user requests to remove a user
    THEN the user is removed
    """
    users = User.objects.all()
    assert len(users) == 0

    email = fake.email()
    password = fake.password(length=16)
    first_name = fake.first_name()
    last_name = fake.last_name()

    user = add_custom_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    url = reverse("user-detail", args=[user.slug])

    res = client.get(url)

    assert res.status_code == status.HTTP_200_OK

    users = User.objects.all()
    assert len(users) == 1

    res_delete = client.delete(url)

    assert res_delete.status_code == status.HTTP_204_NO_CONTENT

    users = User.objects.all()
    assert len(users) == 0

    url_retrieve = reverse("user-detail", args=[user.slug])

    res_retrieve = client.get(url_retrieve)

    assert res_retrieve.status_code == status.HTTP_404_NOT_FOUND

    users = User.objects.all()
    assert len(users) == 0

    url_retrieve = reverse("user-list")

    res_retrieve_list = client.get(url_retrieve)

    assert res_retrieve_list.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_remove_custom_user_incorrect_id(client, add_custom_user):
    """
    GIVEN a Django application
    WHEN the user requests to remove a user with an incorrect id
    THEN the user is not found, a 404 is returned
    """
    users = User.objects.all()
    assert len(users) == 0

    email = fake.email()
    password = fake.password(length=16)
    first_name = fake.first_name()
    last_name = fake.last_name()

    add_custom_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    invalid_id = 12457

    users = User.objects.all()
    assert len(users) == 1

    url = reverse("user-detail", args=[invalid_id])

    res = client.delete(url)

    assert res.status_code == status.HTTP_404_NOT_FOUND

    users = User.objects.all()
    assert len(users) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {
            "payload": {
                "email": fake.email(),
                "password": "abcdefghij123!+-",
                "first_name": "Nick",
                "last_name": "Miller",
            }
        },
        {
            "payload": {
                "email": "nick@testuser.com",
                "password": fake.password(length=16),
                "first_name": "Nick",
                "last_name": "Miller",
            }
        },
        {
            "payload": {
                "email": "nick@testuser.com",
                "password": "abcdefghij123!+-",
                "first_name": fake.first_name(),
                "last_name": "Miller",
            }
        },
        {
            "payload": {
                "email": "nick@testuser.com",
                "password": "abcdefghij123!+-",
                "first_name": "Nick",
                "last_name": fake.last_name(),
            }
        },
        {
            "payload": {
                "email": fake.email(),
                "password": fake.password(length=16),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
            }
        },
    ],
)
def test_update_custom_user(client, add_custom_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to update a user
    THEN the user is updated
    """
    users = User.objects.all()
    assert len(users) == 0

    email = "nick@testuser.com"
    password = "abcdefghij123!+-"
    first_name = "Nick"
    last_name = "Miller"

    user = add_custom_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    users = User.objects.all()
    assert len(users) == 1

    url = reverse("user-detail", args=[user.slug])

    res = client.put(
        url,
        test_data["payload"],
        content_type="application/json",
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data["email"] == test_data["payload"]["email"]
    assert res.data["first_name"] == test_data["payload"]["first_name"]
    assert res.data["last_name"] == test_data["payload"]["last_name"]

    users = User.objects.all()
    assert len(users) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {
            "payload": {
                "email": "nick@testuser.com",
                "password": "abcdefghij123!+-",
                "first_name": fake.first_name(),
                "last_name": "Miller",
            },
            "invalid_id": 12547,
        }
    ],
)
def test_update_custom_user_incorrect_id(client, add_custom_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to update a user with an incorrect id
    THEN the user is not found, a 404 is returned
    """
    email = "nick@testuser.com"
    password = "abcdefghij123!+-"
    first_name = "Nick"
    last_name = "Miller"

    add_custom_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    url = reverse("user-detail", args=[test_data["invalid_id"]])

    res = client.put(
        url, test_data["payload"], content_type="application/json"
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
@pytest.mark.parametrize(
    "test_data",
    [
        {
            "payload": {
                "email": fake.email(),
                "password": "abcdefghij123!+-",
                "first name": "Nick",
                "last name": "Miller",
            }
        },
        {
            "payload": {
                "password": "abcdefghij123!+-",
                "first_name": fake.first_name(),
                "last_name": "Miller",
            }
        },
        {
            "payload": {
                "email": "nick@testuser.com",
                "password": "abcdefghij123!+-",
                "last_name": fake.last_name(),
            }
        },
    ],
)
def test_update_custom_user_invalid_data(client, add_custom_user, test_data):
    """
    GIVEN a Django application
    WHEN the user requests to update a user with invalid data
    THEN the user is not updated, a 404 is returned
    """
    users = User.objects.all()
    assert len(users) == 0

    email = "nick@testuser.com"
    password = "abcdefghij123!+-"
    first_name = "Nick"
    last_name = "Miller"

    user = add_custom_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    users = User.objects.all()
    assert len(users) == 1

    url = reverse("user-detail", args=[user.slug])

    res = client.put(
        url, test_data["payload"], content_type="application/json"
    )

    assert res.status_code == status.HTTP_400_BAD_REQUEST
