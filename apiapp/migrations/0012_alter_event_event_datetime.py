# Generated by Django 4.0.3 on 2022-06-16 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0011_alter_event_event_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_datetime',
            field=models.DateTimeField(),
        ),
    ]
