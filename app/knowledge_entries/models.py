from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class KnowledgeEntry(models.Model):
    """
    KnowledgeEntry model to allow users to create knowledge entries
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="knowledge_entries",
    )
    content = RichTextField(_("Knowledge Entry"))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def created_on_date(self):
        """
        Returns the date the knowledge entry was created
        """
        return self.created_on.date

    class Meta:
        """
        Meta options for the KnowledgeEntry model
        """

        verbose_name_plural = "Knowledge Entries"
        ordering = ["created_on"]
