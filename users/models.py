from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom user model where email is the the unique identifier instead of username
    for authentication instead of username
    """
    username = None
    email = models.EmailField(_("Email"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
