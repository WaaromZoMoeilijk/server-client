# Generated by Django 3.2 on 2021-04-27 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pidjango', '0003_rename_xuser_yuser'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Yuser',
            new_name='Xuser',
        ),
    ]
