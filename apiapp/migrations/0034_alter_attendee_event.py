# Generated by Django 4.0.3 on 2022-06-26 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0033_alter_attendance_options_alter_attendee_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apiapp.event'),
        ),
    ]
