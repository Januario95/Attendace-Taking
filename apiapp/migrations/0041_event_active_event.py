# Generated by Django 4.0.3 on 2022-07-05 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0040_alter_attendance_attendee'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='active_event',
            field=models.BooleanField(default=False),
        ),
    ]
