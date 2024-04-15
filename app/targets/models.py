from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class TargetEntry(models.Model):
    """
    TargetEntry model to allow users to create target entries
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="target_entries",
    )
    title = models.CharField(_("Target"), max_length=255)
    order = models.IntegerField(_("Order"))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # @property decorator transforms the method into a getter method
    # for a specific property
    # https://www.geeksforgeeks.org/python-property-decorator-property/
    @property
    def created_on_date(self):
        """
        Returns the date the target entry was created
        """
        return self.created_on.date

    class Meta:
        """
        Meta options for the TargetEntry model
        """

        verbose_name_plural = "Target Entries"
        ordering = ["order"]

    def __str__(self):
        return self.title
