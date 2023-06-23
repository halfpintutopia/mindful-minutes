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

    class Meta:
        """
        Meta options for the UserSettings model
        """
        verbose_name_plural = "Users' Settings"


class AppointmentEntry(models.Model):
    """
    Appointment entry model to allow users to create appointment entries
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_entries"
    )
    title = models.CharField(_("Title"), max_length=255)
    date = models.DateField(_("Date"))
    time_from = models.TimeField(_("From"))
    time_until = models.TimeField(_("Until"))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """_
        Meta options for the AppointmentEntry model
        """
        verbose_name_plural = "Appointment Entries"
        ordering = ["-date", "-time_from"]

    def clean(self):
        """
        Custom validation to ensure the time_from is less than the time_until
        """
        if self.time_from > self.time_until:
            raise ValidationError(
                _("'From' must start before the time set on 'Until'.")
            )
        return super().clean()

    def __str__(self):
        return self.title


class Target(models.Model):
    """
    Target model to allow users to create targets
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="targets"
    )
    title = models.CharField(_("Target"), max_length=255)
    order = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta options for the Target model
        """
        verbose_name_plural = "Targets"
        ordering = ["created_on"]

    def __str__(self):
        return self.title
