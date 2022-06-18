# Generated by Django 4.0.3 on 2022-06-16 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apiapp', '0009_auto_20210618_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=128)),
                ('event_datetime', models.DateTimeField(auto_now=True)),
                ('event_location', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendee_name', models.CharField(max_length=128)),
                ('attendee_ic', models.CharField(max_length=128)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiapp.event')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_name', models.CharField(max_length=128)),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
                ('attendees', models.ManyToManyField(to='apiapp.attendee')),
            ],
        ),
    ]
