# Generated by Django 4.0.3 on 2022-06-27 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0038_remove_attendance_attendee_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TableAlert',
        ),
        migrations.DeleteModel(
            name='TableDevice',
        ),
    ]