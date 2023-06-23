# Generated by Django 4.2.2 on 2023-06-22 22:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('date', models.DateField(verbose_name='Date')),
                ('time_from', models.TimeField(verbose_name='From')),
                ('time_until', models.TimeField(verbose_name='Until')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_entries', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date', '-time_from'],
            },
        ),
    ]