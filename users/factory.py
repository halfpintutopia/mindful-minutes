# import factory
# from django.contrib.auth import get_user_model
# from faker import Factory
# from ..models import CustomUser, Settings
# from itertools import count

# User = get_user_model()
# faker = Factory.create()
# counter = count()


# class UserFactory(factory.django.DjangoModelFactory):
#     """
#     Factory class for creating User instances
#     """
#     class Meta:
#         """
#         Meta options for the User model
#         """
#         model = CustomUser
#     first_name = factory.LazyAttribute(lambda _: faker.first_name())
#     last_name = factory.LazyAttribute(lambda _: faker.last_name())
#     email = factory.LazyAttribute(lambda _: f'{faker.email()}{next(counter)}')
#     password = factory.LazyAttribute(lambda _: faker.password())


# class SuperUserFactory(factory.django.DjangoModelFactory):
#     """
#     Factory class for creating super user instances
#     """
#     class Meta:
#         """
#         Meta options for the User model
#         """
#         model = CustomUser
#     first_name = faker.first_name()
#     last_name = faker.last_name()
#     email = faker.email()
#     password = faker.password()
#     is_staff = True
#     is_active = True
#     is_superuser = True


# class SettingsFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Settings
#     user = UserFactory()
#     start_week_day = 1
#     morning_check_in = "09:00:00"
#     evening_check_in = "19:00:00"
