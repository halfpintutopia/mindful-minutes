from django.conf import settings
from django.db import models


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
