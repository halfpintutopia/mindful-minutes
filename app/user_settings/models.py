from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


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
        related_name="custom_user_settings",
    )
    start_week_day = models.IntegerField(
        _("Start Week Day"), choices=DAY_OPTIONS
    )
    morning_check_in = models.TimeField()
    evening_check_in = models.TimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta options for the UserSettings model
        """

        verbose_name_plural = "Users' Settings"
