# Generated by Django 3.2.2 on 2021-05-16 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xx', '0018_auto_20210516_0450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpi',
            name='last_reboot',
            field=models.CharField(blank=True, max_length=24, null=True),
        ),
        migrations.AlterField(
            model_name='rpi',
            name='ping_response_time',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]