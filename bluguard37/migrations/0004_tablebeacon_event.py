# Generated by Django 4.0.3 on 2022-06-26 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0036_remove_event_beacon'),
        ('bluguard37', '0003_tablebeacon'),
    ]

    operations = [
        migrations.AddField(
            model_name='tablebeacon',
            name='event',
            field=models.ManyToManyField(to='apiapp.event'),
        ),
    ]
