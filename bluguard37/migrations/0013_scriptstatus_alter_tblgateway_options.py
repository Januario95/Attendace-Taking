# Generated by Django 4.0.3 on 2022-07-03 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluguard37', '0012_alter_tablealert_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScriptStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(default='OFFLINE', max_length=50)),
            ],
            options={
                'verbose_name': 'Script Status',
                'verbose_name_plural': 'Script Status',
            },
        ),
        migrations.AlterModelOptions(
            name='tblgateway',
            options={'ordering': ('-gateway_status',), 'verbose_name': 'Table Device Gateway', 'verbose_name_plural': 'Table Device Gateway'},
        ),
    ]