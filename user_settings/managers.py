from datetime import time

from django.db import models
from django.db.models import Manager
from django.utils.translation import gettext_lazy as _


class UserSettingsManager(Manager):
    """
    User settings model manager to create the settings for the user
    """

    def create_user_settings(self, user, start_week_day, morning_check_in, evening_check_in):
        """
        Create and save the user settings with the given start week day,
        morning check in and evening check in

        Args:
            user (CustomUser)
            start_week_day (int)
            morning_check_in (datetime.time)
            evening_check_in (datetime.time)
        """
        if not start_week_day:
            raise ValueError(_("The start week day should not be blank."))
        if not isinstance(start_week_day, int):
            raise ValueError(_("The option is not an integer between 1-7."))
        if not morning_check_in:
            raise ValueError(_("The morning check in should not be blank."))
        if not isinstance(morning_check_in, time):
            raise ValueError(
                _("The morning check in should be in time format."))
        if not evening_check_in:
            raise ValueError(_("The evening check in should not be blank."))
        if not isinstance(evening_check_in, time):
            raise ValueError(
                _("The evening check in should be in time format."))
        # user_settings = self.create() # saves the newly created instance to the database
        user_settings = self.model(
            user=user,
            start_week_day=start_week_day,
            morning_check_in=morning_check_in,
            evening_check_in=evening_check_in
        )
        user_settings.save()
        return user_settings
