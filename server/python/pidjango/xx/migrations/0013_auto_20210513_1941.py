# Generated by Django 3.2.2 on 2021-05-13 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xx', '0012_auto_20210513_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpi',
            name='status',
            field=models.CharField(choices=[('active', 'active'), ('blocked', 'blocked')], default='initial', max_length=12),
        ),
        migrations.AlterField(
            model_name='rpiclicommand',
            name='response',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
