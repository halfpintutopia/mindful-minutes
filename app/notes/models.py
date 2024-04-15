from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class NoteEntry(models.Model):
    """
    NoteEntry model to allow users to create note entries
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="note_entries",
    )
    content = models.TextField(_("Notes"))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def created_on_date(self):
        """
        Returns the date the note entry that was created
        """
        return self.created_on.date

    class Meta:
        """
        Meta options for the TargetEntry model
        """

        verbose_name_plural = "Note Entries"
        ordering = ["created_on"]
