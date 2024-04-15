# Generated by Django 4.2.2 on 2024-03-01 14:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EmotionEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "emotion",
                    models.CharField(
                        choices=[
                            ("awful", "Awful"),
                            ("terrible", "Terrible"),
                            ("bad", "Bad"),
                            ("okay", "Okay"),
                            ("good", "Good"),
                            ("great", "Great"),
                            ("excellent", "Excellent"),
                        ],
                        max_length=10,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="emotion_entries",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Emotion Entries",
                "ordering": ["created_on"],
            },
        ),
    ]
