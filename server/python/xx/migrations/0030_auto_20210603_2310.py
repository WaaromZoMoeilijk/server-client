# Generated by Django 3.2.2 on 2021-06-03 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xx', '0029_xuser_password2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xuser',
            name='password',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='password2',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]