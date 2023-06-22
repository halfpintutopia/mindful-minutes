from datetime import time

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
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


class UserSettings(models.Model):
    """
    User settings model to allow users set their start week day
    and check in times for morning and evening
    """
    DAY_OPTIONS = [
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_settings"
    )
    start_week_day = models.IntegerField(
        _("Start Week Day"), choices=DAY_OPTIONS)
    morning_check_in = models.TimeField()
    evening_check_in = models.TimeField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
