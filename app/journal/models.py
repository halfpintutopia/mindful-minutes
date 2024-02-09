import uuid

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom user model where email is the unique identifier
    instead of username for authentication instead of username
    """

    username = None
    email = models.EmailField(_("Email"), unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    unique_identifier = models.UUIDField(default=uuid.uuid4, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_name = slugify(f"{self.first_name} {self.last_name}")
            slug = f"{slug_name}-{str(self.unique_identifier)}"

            duplicates = CustomUser.objects.filter(slug=slug).exclude(pk=self.pk)

            while duplicates.exists():
                self.unique_identifier = uuid.uuid4()
                slug = f"{slug_name}-{self.unique_identifier}"

                duplicates = CustomUser.objects.filter(slug=slug).exclude(pk=self.pk)

            self.slug = slug

        super().save(*args, **kwargs)

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
        related_name="user_settings",
    )
    start_week_day = models.IntegerField(_("Start Week Day"), choices=DAY_OPTIONS)
    morning_check_in = models.TimeField()
    evening_check_in = models.TimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

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


class NoteEntry(models.Model):
    """
    NoteEntry model to allow users to create note entries
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="note_entries",
    )
    content = RichTextField(_("Notes"))
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


class GratitudeEntry(models.Model):
    """
    GratitudeEntry model to allow users to create gratitude entries
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gratitude_entries",
    )
    content = RichTextField(_("Gratitude Entry"))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def created_on_date(self):
        """
        Returns the date the gratitude entry was created
        """
        return self.created_on.date

    class Meta:
        """
        Meta options for the Target model
        """

        verbose_name_plural = "Gratitude Entries"
        ordering = ["created_on"]


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


class IdeasEntry(models.Model):
    """
    IdeasEntry model to allow users to create ideas entries
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ideas_entries",
    )
    content = RichTextField(_("Ideas Entry"))
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def created_on_date(self):
        """
        Returns the date the ideas entry was created
        """
        return self.created_on.date

    class Meta:
        """
        Meta options for the IdeaEntry model
        """

        verbose_name_plural = "Ideas Entries"
        ordering = ["created_on"]


class ImprovementEntry(models.Model):
    """
    ImprovementEntry model to allow users to create improvement entries
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="improvement_entries",
    )
    content = RichTextField(_("Improvement Entry"))
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


class EmotionEntry(models.Model):
    """
    EmotionEntry model to allow users to create improvement entries
    """

    EMOTION_CHOICES = [
        ("awful", "Awful"),
        ("terrible", "Terrible"),
        ("bad", "Bad"),
        ("okay", "Okay"),
        ("good", "Good"),
        ("great", "Great"),
        ("excellent", "Excellent"),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="emotion_entries",
    )
    emotion = models.CharField(max_length=10, choices=EMOTION_CHOICES)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def created_on_date(self):
        """
        Returns the date the emotion entry was created
        """
        return self.created_on.date

    class Meta:
        """
        Meta options for the EmotionEntry model
        """

        verbose_name_plural = "Emotion Entries"
        ordering = ["created_on"]
