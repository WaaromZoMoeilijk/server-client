# Generated by Django 3.2.2 on 2021-05-23 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xx', '0021_auto_20210523_0123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='xuser',
            name='address1',
        ),
        migrations.RemoveField(
            model_name='xuser',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='xuser',
            name='bankaccount',
        ),
        migrations.RemoveField(
            model_name='xuser',
            name='btw_number',
        ),
        migrations.RemoveField(
            model_name='xuser',
            name='city',
        ),
        migrations.RemoveField(
            model_name='xuser',
            name='coc_number',
        ),
        migrations.RemoveField(
            model_name='xuser',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='xuser',
            name='last_bill',
        ),
        migrations.RemoveField(
            model_name='xuser',
            name='swiftcode',
        ),
        migrations.RemoveField(
            model_name='xuser',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='xuser',
            name='activation_code',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
