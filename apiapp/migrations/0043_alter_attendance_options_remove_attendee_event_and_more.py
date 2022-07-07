# Generated by Django 4.0.3 on 2022-07-06 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0042_alter_attendee_options_alter_event_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'ordering': ['-check_in_date'], 'verbose_name': 'Table Attendance', 'verbose_name_plural': 'Table Attendance'},
        ),
        migrations.RemoveField(
            model_name='attendee',
            name='event',
        ),
        migrations.AddField(
            model_name='event',
            name='attendee',
            field=models.ManyToManyField(to='apiapp.attendee'),
        ),
    ]