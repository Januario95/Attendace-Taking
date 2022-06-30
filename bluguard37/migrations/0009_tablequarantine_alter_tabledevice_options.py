# Generated by Django 4.0.3 on 2022-06-29 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluguard37', '0008_tablealert'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableQuarantine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_tag', models.CharField(blank=True, max_length=50, null=True)),
                ('device_mac', models.CharField(blank=True, max_length=100, null=True)),
                ('device_type', models.CharField(default='HSWB004', max_length=100)),
                ('device_status', models.CharField(blank=True, max_length=20, null=True)),
                ('device_assignment', models.CharField(blank=True, max_length=30, null=True)),
                ('device_temp', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('device_o2', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('device_bat', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('device_hr', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('last_read_date', models.DateField(blank=True, null=True)),
                ('last_read_time', models.TimeField(blank=True, null=True)),
                ('incorrect_data_flag', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Table Quarantine',
                'verbose_name_plural': 'Table Quarantine',
                'ordering': ('-device_status',),
            },
        ),
        migrations.AlterModelOptions(
            name='tabledevice',
            options={'ordering': ('-device_status',), 'verbose_name': 'Device', 'verbose_name_plural': 'Table Device'},
        ),
    ]
