# Generated by Django 4.2.10 on 2024-03-12 18:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("targets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="targetentry",
            name="completed",
            field=models.BooleanField(default=False, verbose_name="Completed"),
        ),
    ]
