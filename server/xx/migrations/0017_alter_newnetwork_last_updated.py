# Generated by Django 3.2.2 on 2021-05-15 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xx', '0016_alter_rpiclicommand_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newnetwork',
            name='last_updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
