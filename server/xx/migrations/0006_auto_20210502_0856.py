# Generated by Django 3.2 on 2021-05-02 08:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xx', '0005_auto_20210501_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='country',
            field=models.CharField(choices=[('nl', 'Netherlands'), ('be', 'Belgium'), ('ae', 'United Arabic Emirates'), ('uk', 'United Kingdom'), ('us', 'United States')], default='nl', max_length=2),
        ),
        migrations.AlterField(
            model_name='customer',
            name='language',
            field=models.CharField(choices=[('nl', 'Dutch'), ('en', 'English')], max_length=2),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='last_login',
            field=models.DateTimeField(),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('initial', 'initial'), ('sent', 'sent'), ('paid', 'paid'), ('cancelled', 'cancelled')], default='initial', max_length=10)),
                ('paid_date', models.DateTimeField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xx.customer')),
            ],
        ),
    ]
