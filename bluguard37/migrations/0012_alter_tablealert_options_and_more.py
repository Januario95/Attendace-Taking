# Generated by Django 4.0.3 on 2022-07-02 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluguard37', '0011_alter_tablealldevices_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tablealert',
            options={'ordering': ('-id',), 'verbose_name': 'Table Alert', 'verbose_name_plural': 'Table Alert'},
        ),
        migrations.AlterField(
            model_name='tblgateway',
            name='last_updated_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]