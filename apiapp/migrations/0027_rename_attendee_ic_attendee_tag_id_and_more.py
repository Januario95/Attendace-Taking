# Generated by Django 4.0.3 on 2022-06-17 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0026_rename_event_datetime_event_start_datetime_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='attendee',
            old_name='attendee_ic',
            new_name='tag_id',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='check_in',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='check_out',
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='device_mac',
        ),
        migrations.AddField(
            model_name='attendee',
            name='check_in_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendee',
            name='check_in_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendee',
            name='check_out_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attendee',
            name='check_out_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
