# Generated by Django 4.0.3 on 2022-07-05 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0041_event_active_event'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendee',
            options={'ordering': '', 'verbose_name': 'Table Attendee', 'verbose_name_plural': 'Table Attendee'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-last_updated',), 'verbose_name': 'Table Event', 'verbose_name_plural': 'Table Event'},
        ),
        migrations.AddField(
            model_name='event',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
