from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class WinEntry(models.Model):
    """
    Win model to allow users to create win entries
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="win_entries",
    )
    title = models.CharField(_("Win Entry"), max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def created_on_date(self):
        """
        Returns the date the win entry was created
        """
        return self.created_on.date

    class Meta:
        """
        Meta options for the Win model
        """

        verbose_name_plural = "Win Entries"
        ordering = ["created_on"]
