# Generated by Django 3.2.2 on 2021-05-13 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xx', '0009_auto_20210505_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rpi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('computernr', models.CharField(max_length=24)),
                ('activation_code', models.CharField(blank=True, max_length=12, null=True)),
                ('softwareVersion', models.CharField(default='00000', max_length=5)),
                ('wifiAvailableNetworks', models.CharField(blank=True, max_length=256, null=True)),
                ('wifiCurrentNetwork', models.CharField(blank=True, max_length=36, null=True)),
                ('wifiKnownNetworks', models.CharField(blank=True, max_length=256, null=True)),
                ('ipAddressWlan', models.CharField(blank=True, max_length=36, null=True)),
                ('ipAddressEth', models.CharField(blank=True, max_length=36, null=True)),
                ('ipAddressWAN', models.CharField(blank=True, max_length=36, null=True)),
                ('ping_response_time', models.IntegerField(blank=True, null=True)),
                ('sd_card', models.CharField(blank=True, max_length=36, null=True)),
                ('last_reboot', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('initial', 'initial'), ('active', 'active'), ('blocked', 'blocked')], default='initial', max_length=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_seen', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='xuser',
            name='activation_code_nw_email',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='xuser',
            name='new_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='xuser',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('regular', 'regular')], default='regular', max_length=12),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='address1',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='address2',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='bankaccount',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='btw_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='coc_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='company_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='last_bill',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='password',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='swiftcode',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='userid',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='xuser',
            name='zipcode',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.CreateModel(
            name='RpiLogline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('rpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xx.rpi')),
            ],
        ),
        migrations.CreateModel(
            name='RpiCliCommand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent', models.CharField(max_length=500)),
                ('response', models.DateTimeField(blank=True, max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('rpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xx.rpi')),
            ],
        ),
        migrations.CreateModel(
            name='NewNetwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssid', models.CharField(max_length=500)),
                ('newssid', models.CharField(blank=True, max_length=36, null=True)),
                ('password', models.CharField(blank=True, max_length=36, null=True)),
                ('wlan_dhcp_fixed', models.CharField(choices=[('dhcp', 'dhcp'), ('fixed', 'fixed')], default='dhcp', max_length=5)),
                ('wlan_static_IP', models.CharField(blank=True, max_length=36, null=True)),
                ('wlan_router', models.CharField(blank=True, max_length=36, null=True)),
                ('wlan_network_domain', models.CharField(blank=True, max_length=36, null=True)),
                ('eth_dhcp_fixed', models.CharField(choices=[('dhcp', 'dhcp'), ('fixed', 'fixed')], default='dhcp', max_length=5)),
                ('eth_static_IP', models.CharField(blank=True, max_length=36, null=True)),
                ('eth_router', models.CharField(blank=True, max_length=36, null=True)),
                ('eth_network_domain', models.CharField(blank=True, max_length=36, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('rpi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xx.rpi')),
            ],
        ),
    ]