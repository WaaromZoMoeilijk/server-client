# Generated by Django 3.2 on 2021-05-05 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pidjango', '0009_invoiceline'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='bill_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='sent_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='xuser',
            name='address1',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='xuser',
            name='address2',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='xuser',
            name='bankaccount',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='xuser',
            name='city',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='xuser',
            name='company_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='xuser',
            name='last_bill',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='xuser',
            name='swiftcode',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AddField(
            model_name='xuser',
            name='zipcode',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('initial', 'initial'), ('sent', 'sent'), ('paid', 'paid'), ('canceled', 'canceled')], default='initial', max_length=10),
        ),
    ]
