# Generated by Django 4.0.3 on 2022-06-26 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluguard37', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_tag', models.CharField(blank=True, max_length=50, null=True)),
                ('device_mac', models.CharField(blank=True, max_length=100, null=True)),
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
                'verbose_name': 'Device',
                'verbose_name_plural': 'Table Device',
            },
        ),
        migrations.AlterModelOptions(
            name='tblalertcode',
            options={'verbose_name': 'Table Alert', 'verbose_name_plural': 'Table Alert'},
        ),
        migrations.AlterModelOptions(
            name='tbldevicerawlength',
            options={'verbose_name': 'Table Device Raw Length', 'verbose_name_plural': 'Table Device Raw Length'},
        ),
        migrations.AlterModelOptions(
            name='tblgateway',
            options={'verbose_name': 'Table Device Gateway', 'verbose_name_plural': 'Table Device Gateway'},
        ),
    ]
