from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .managers import UserSettingsManager


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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_week_day = models.IntegerField(
        _("Start Week Day"), choices=DAY_OPTIONS)
    morning_check_in = models.TimeField(_("Morning Check In"))
    evening_check_in = models.TimeField(_("Evening Check In"))

    # objects is the common name used for the default manager of the model,
    # to perform database operations and instances on the models
    objects = UserSettingsManager()
