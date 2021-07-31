import json, os, datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE','pidjango.settings')

import django
django.setup()
from xx.models import Rpi

rpis = Rpi.objects.all()
def run():
	for rpi in rpis:
		rpi_info = {}
		filename = rpi.xuser.userid + '-' + str(rpi.id)
		rpi_info['id'] = rpi.id
		rpi_info['ipAddressEth'] = rpi.ipAddressEth
		rpi_info['ipAddressWlan'] = rpi.ipAddressWlan
		rpi_info['gateway'] = rpi.gateway
		rpi_info['subnetWlan'] = rpi.subnetWlan
		rpi_info['subnetEth'] = rpi.subnetEth
		rpi_info['nameserver'] = rpi.nameserver
		rpi_info['wifiCurrentNetwork'] = rpi.wifiCurrentNetwork
		rpi_info['ssh_port'] = rpi.ssh_port
		rpi_info['computernr'] = rpi.computernr
		rpi_info['version'] = rpi.version
		rpi_info['sd_card'] = rpi.sd_card
		rpi_info['user_id'] = rpi.xuser.id
		rpi_info['userid'] = rpi.xuser.userid
		rpi_info['email'] = rpi.xuser.email
		sstr = rpi.last_seen
		rpi_info['last_seen'] = sstr.strftime('%Y%m%d%H%M')
		print(json.dumps(rpi_info))
		f = open('/home/pi/rpi_info/' + filename + '.json', 'w+')
		f.write(json.dumps(rpi_info))
		f.close()
run()
