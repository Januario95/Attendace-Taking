# Generated by Django 4.0.3 on 2022-06-16 16:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0015_attendee_mac_alter_attendee_check_in_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='check_in',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 16, 16, 27, 46, 146750)),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='check_out',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 16, 16, 27, 46, 146750)),
        ),
    ]
