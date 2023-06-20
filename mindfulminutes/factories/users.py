import factory
from django.contrib.auth import get_user_model
from faker import Factory

User = get_user_model()
faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating User instances
    """
    class Meta:
        """
        Meta options for the User model
        """
        model = User
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()
    password = faker.password()


class SuperUserFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating super user instances
    """
    class Meta:
        """
        Meta options for the User model
        """
        model = User
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()
    password = faker.password()
    is_staff = True
    is_active = True
    is_superuser = True
