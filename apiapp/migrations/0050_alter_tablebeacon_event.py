# Generated by Django 4.0.6 on 2022-07-07 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0049_alter_event_attendee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablebeacon',
            name='event',
            field=models.ManyToManyField(blank=True, null=True, to='apiapp.event'),
        ),
    ]