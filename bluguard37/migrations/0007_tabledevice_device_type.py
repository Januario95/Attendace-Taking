# Generated by Django 4.0.3 on 2022-06-27 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluguard37', '0006_alter_tblalertcode_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabledevice',
            name='device_type',
            field=models.CharField(default='HSWB004', max_length=100),
        ),
    ]
