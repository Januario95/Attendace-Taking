# Generated by Django 4.0.3 on 2022-06-17 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0025_remove_attendance_attendance_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_datetime',
            new_name='start_datetime',
        ),
        migrations.AddField(
            model_name='event',
            name='end_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_sublocation',
            field=models.CharField(default='Singapore', max_length=128),
        ),
    ]
