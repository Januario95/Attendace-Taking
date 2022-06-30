# Generated by Django 4.0.3 on 2022-06-26 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0037_tablebeacon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='attendee_name',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='event',
        ),
        migrations.AddField(
            model_name='attendance',
            name='attendee',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='apiapp.attendee'),
        ),
    ]
