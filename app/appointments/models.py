from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class AppointmentEntry(models.Model):
    """
    Appointment entry model to allow users to create appointment entries
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointment_entries",
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
        ordering = ["date", "time_from"]

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