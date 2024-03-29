# Generated by Django 4.0.3 on 2022-06-18 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiapp', '0028_tabledevice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tabledevice',
            name='device_assignment',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='tabledevice',
            name='device_bat',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='tabledevice',
            name='device_hr',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='tabledevice',
            name='device_mac',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='tabledevice',
            name='device_o2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='tabledevice',
            name='device_status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='tabledevice',
            name='device_tag',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tabledevice',
            name='device_temp',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='tabledevice',
            name='last_read_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tabledevice',
            name='last_read_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
