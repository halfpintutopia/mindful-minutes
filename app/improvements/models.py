from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class ImprovementEntry(models.Model):
    """
    ImprovementEntry model to allow users to create improvement entries
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="improvement_entries",
    )
    content = models.TextField(_("Improvement Entry"))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def created_on_date(self):
        """
        Returns the date the improvement entry was created
        """
        return self.created_on.date

    class Meta:
        """
        Meta options for the ImprovementEntry model
        """

        verbose_name_plural = "Improvement Entries"
        ordering = ["created_on"]
