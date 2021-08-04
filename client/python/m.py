from time import sleep
import os.path, time
import os
import datetime
import subprocess
import sys
import requests
from ffunctions import *

# Temporary suppression of SSL warnings
urllib3.disable_warnings()

try:
	sysargv = sys.argv[1]
except:
	sysargv = ''

class sendtoserver:
# this class manages the information that should be delivered to the server with the next call
	def __init__(self):
		sstr = 'have to do something here'

	def add(self,jobname,id,response=''):
		sendtoserver = cf.read('sendtoserver')
		if not isinstance(sendtoserver, list):
			sendtoserver = []
		sendtoserver.append({"jobname": jobname, "id": id, "response": response})
		cf.check_update_config('sendtoserver',sendtoserver)

	def empty(self):
		cf.check_update_config('sendtoserver','')

	def len(self):
		return len(cf.read('sendtoserver'))

cf = configtxt()
ssm = system_info()
sts = sendtoserver()
now = datetime.datetime.now()

if os.path.isfile('/dev/shm/frequency'):
	f = open('/dev/shm/frequency', 'r')
	runteller = f.read()
	f.close()
	runteller = int(runteller.rstrip())
else:
	runteller = 0

if int(runteller) > 30 and ssm.comp_nr_only_dec %10 != now.minute % 10 and cf.read('activation_code') == '':
	print('too little happening')
	sys.exit()

try:
	procesloopt_a_py = 0
	procesloopt_m_py = 0
	ps = subprocess.run(['ps', 'aux'], capture_output=True, text=True).stdout
	processes = ps.split('\n')
	for row in processes:
		if 'python3 /home/dietpi/a.py' in str(row):
			procesloopt_a_py = 1
			print('found in ps aux:' + row)
		if 'python3 /home/dietpi/m.py' in str(row):
			procesloopt_m_py += 1
			print('found in ps aux:' + row)
	if procesloopt_a_py == 0 and sysargv == '':
		os.system('sudo python3 /home/dietpi/a.py &')
		addtopermlog('a.py started')
	else:
		print('dont start: a.py running already')
	if procesloopt_m_py > 1 and sysargv == '':
		addtopermlog(' this m.py stopped: an older m.py is still running')
		f = open('/dev/shm/m_py_last_start', 'r')
		sstr = f.read()
		f.close()
		sstr = sstr.rstrip()
		if int(sstr) + 600 < time.time():
			addtopermlog('m.py runs more than 10 minutes. Lets reboot.')
			# hier ook alle openstaande clicommands klaarmelden met overtime.
			os.system('sudo reboot')
		sys.exit()
	else:
		f = open('/dev/shm/m_py_last_start', 'w+')
		f.write(str(int(time.time())))
		f.close()
except:
	print('something wrong')

# next is the update routine. Should be based on github. Still to be done.
if now.hour == 11 and int(ssm.comp_nr_only_dec)%60 == now.minute:
	sleep(int(ssm.comp_nr_only_dec)%31)
	os.system("sudo python /home/dietpi/update.py wzm &")
if cf.read('version') != '' and now.hour == 11 and now.minute == 0:
	os.system("sudo cp /home/dietpi/config.txt /home/dietpi/configres.txt &")
	addtosessionlog('copied config.txt to configres.txt')
if now.hour == 6 and now.minute == 0:
	os.system("sudo rm /dev/shm/log.txt &")

ourserver = cf.read('ourserver')
if ourserver == '':
	ourserver = 'https://wzc.waaromzomoeilijk.nl:2021'
if ourserver[:4] != 'http':
	ourserver = 'https://' + ourserver

cf.check_update_config('ipAddressWlan', ssm.wlanIPaddress)
cf.check_update_config('ipAddressEth', ssm.ethIPaddress)
cf.check_update_config('wifiCurrentNetwork', ssm.wifiCurrentNetwork)
ps = subprocess.run(["route","-n"], capture_output=True, text=True).stdout
ps = ps.split("\n")
gateway = ''
for sstr in ps:
	print('sstr:' + sstr + 'x')
	while sstr.replace("  "," ") != sstr:
		sstr = sstr.replace("  "," ")
	sstr = sstr.split(" ")
	if len(sstr) > 1:
		sstr = sstr[1]
		if sstr != '0.0.0.0' and len(sstr.replace('.','')) + 3 == len(sstr):
			gateway = sstr
cf.check_update_config('gateway', gateway) 
if ssm.ethIPaddress == '':
	subnetEth = ''
else:
	subnetEth = ssm.ethIPaddress
	subnetEth = subnetEth.split('.')
	subnetEth = subnetEth[0] + '.' + subnetEth[1] + '.' + subnetEth[2] + '.0'
cf.check_update_config('subnetEth', subnetEth)
if ssm.wlanIPaddress == '':
	subnetWlan = ''
else:
	subnetWlan = ssm.wlanIPaddress
	subnetWlan = subnetWlan.split('.')
	subnetWlan = subnetWlan[0] + '.' + subnetWlan[1] + '.' + subnetWlan[2] + '.0' 
cf.check_update_config('subnetWlan', subnetWlan)
nameserver = ''
f = open('/etc/resolv.conf', 'r')
f = f.readlines()
for sstr in f:
	if sstr[:10] == 'nameserver':
		nameserver = sstr[11:]
	nameserver = nameserver.replace("\n","")
cf.check_update_config('nameserver', nameserver)

netwerkdata = {}
netwerkdata['wifiAvailableNetworks'] = ssm.wifilist
netwerkdata['wifiCurrentNetwork'] = ssm.wifiCurrentNetwork
netwerkdata['wifiKnownNetworks'] = ssm.wifiKnownNetworks
netwerkdata['ipAddressWlan'] = ssm.wlanIPaddress
netwerkdata['ipAddressEth'] = ssm.ethIPaddress
netwerkdata['sd_card'] = ssm.sd_info
netwerkdata['gateway'] = gateway
netwerkdata['subnetEth'] = subnetEth
netwerkdata['subnetWlan'] = subnetWlan
netwerkdata['nameserver'] = nameserver
netwerkdata['ssh_port'] = cf.read('ssh_port')

# send only if something has changed:
if os.path.isfile('/dev/shm/data_str'):
	f = open('/dev/shm/data_str', 'r')
	networkstring_old = f.read()
	f.close()
else:
	networkstring_old = '{}'
networkstring_new = json.dumps(netwerkdata)
if networkstring_old != networkstring_new:
	f = open('/dev/shm/data_str', 'w')
	f.write(networkstring_new)
	f.close()

# get date-time of last reboot
	ps = subprocess.run(['uptime','-s'], capture_output=True, text=True).stdout
	netwerkdata['last_reboot'] = str(ps)[2:].replace("\\n'","").replace("\n","")
# get statistics about ping
	sstr = ourserver.replace('http://','')
	sstr = sstr.replace('https://','')
	ps = subprocess.run(['ping',sstr,'-w','4'], capture_output=True, text=True).stdout
	ps = str(ps)
	ps = ps.split('\\n')
	for row in ps:
		if row[:3] == 'rtt':
			netwerkdata['ping_response_time'] = row
	# example of output:
	# rtt min/avg/max/mdev = 7.549/7.706/7.891/0.150 ms
else:
	netwerkdata = {}

postinfo = netwerkdata
postinfo["computernr"] = ssm.computernr
postinfo["version"] = cf.read('version')
if sts.len() > 0:
	postinfo['sendtoserver'] = cf.read('sendtoserver') # not a nice way. I didnt find another.

api_url_base = ourserver + '/xx/api'
headers = {'Content-Type': 'multipart/form-data'}
postinfo = json.dumps(postinfo)
print('postinfo:' + str(postinfo))
print('url base:' + api_url_base)

# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx  HERE is the API call xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
response = requests.post(api_url_base, headers=headers, data=postinfo, verify=0)
print('content:' + str(response.content))
if response.status_code != 200:
	addtopermlog('can not contact server. status: ' + str(response.status_code))
	sys.exit()
else:
	sts.empty()
	api_answer = json.loads(response.content.decode('utf-8'))
	ssh_port = 12347
	if 'activation_code' in api_answer:      # new system, not yet assigned to a user.
		if cf.check_update_config('activation_code', api_answer['activation_code']) == 'updated':
			ssh_port = 60000 + int(api_answer['id'])
			f = open('/home/dietpi/ssh_port', 'w')
			f.write(str(ssh_port))
			f.close()
			cf.check_update_config('ssh_port', str(ssh_port))
# a.py is responsible for publishing the computernr and activation_code at:
# (1) /var/www/html/index.html/index
# (2) via de HDMI.
	elif cf.check_update_config('activation_code', '') == 'updated':
		ssh_port = 10000 + int(api_answer['id'])
		f = open('/home/dietpi/ssh_port', 'w')
		f.write(str(ssh_port))
		f.close()
		cf.check_update_config('ssh_port', str(ssh_port))

	# next: check the job is done or open:
	if 'newnetwork' in api_answer and api_answer['newnetwork']['id'] > int('0' + str(cf.read('last_newnetwork_job'))):
		print('aaa')
		# next: check correct input for new wifi-credentials
		if api_answer['newnetwork']['newssid'] is not None and api_answer['newnetwork']['newssid'] != '':
			ssid = api_answer['newnetwork']['newssid']
			networkpassword = api_answer['newnetwork']['psk']
			if networkpassword is None:
				networkpassword = ''
			found_ssid = 'no'
			print('aaa2')
			ssidknown = 'no'
			new_wpa_suppl = ''
			write_new_wpa_suppl = 'no'
			f = open( "/etc/wpa_supplicant/wpa_supplicant.conf", "r" )
			for sstr in f:
				if sstr[0:-1] == "  ssid=\"" + ssid +"\"":
					found_ssid = 'yes'
					ssidknown = 'yes'
					new_wpa_suppl += sstr + "  scan_ssid=1\n"
				elif ssidknown == 'yes' and ((sstr[:6] == "  psk=" and sstr[0:-1] != "  psk=\"" + networkpassword +"\"") or (sstr[0:-1] == "  key_mgmt=NONE" and networkpassword != '')):
					# here we know we are reading the line of the password
					if networkpassword == '':
						new_wpa_suppl += "  key_mgmt=NONE\n}\n"
					else:
						new_wpa_suppl += "  psk=\"" + networkpassword +"\"}\n"
					ssidknown = 'no'
					write_new_wpa_suppl = 'yes'
					addtopermlog('Changed existing wifi network.')
				elif sstr[0:11] != "  scan_ssid" and sstr[0:-1] != '':
					new_wpa_suppl += sstr
			print('aaa5')
			if found_ssid == 'no':
				# obviously there is a new SSID
				new_wpa_suppl += "network={\n";
				new_wpa_suppl += "  ssid=\"" + ssid + "\"\n  scan_ssid=1\n";
				if networkpassword != '':
					new_wpa_suppl += "  psk=\"" + networkpassword + "\"\n}\n";
				else:
					new_wpa_suppl += "  key_mgmt=NONE\n}\n";
				write_new_wpa_suppl = 'yes'
				addtopermlog('Wifi network added.')
			if write_new_wpa_suppl == 'yes':
				f = open('/tmp/wpa_s', 'w')
				f.write(new_wpa_suppl)
				f.close()
				os.system('sudo cp /tmp/wpa_s /etc/wpa_supplicant/wpa_supplicant.conf')
		print('aaa7')
		if 'newnetwork' in api_answer:
			f = open('/etc/dhcpcd.conf', 'r')
			content = f.read()
			content = content.split('\n')
			tteller = 0
			new_content = ''
			if api_answer['newnetwork']['eth_dhcp_fixed'] == 'dhcp':
				for row in content:
					if not (row == 'interface eth0' or tteller == 1 or tteller == 2 or tteller == 3):
						if new_content != '':
							new_content += "\n"
						new_content += row
					else:
						tteller += 1
				content = new_content.split('\n')
			elif api_answer['newnetwork']['eth_dhcp_fixed'] == 'static':
				for row in content:
					if not (row == 'interface eth0' or tteller == 1 or tteller == 2 or tteller == 3):
						if new_content != '':
							new_content += "\n"
						new_content += row
					else:
						tteller += 1
				new_content += "interface eth0\n"
				sstr = api_answer['newnetwork']['eth_static_IP']
				if not '/' in sstr:
					sstr += "/24"
				new_content += "static ip_address=" + sstr + "\n"
				new_content += "static routers=" + api_answer['newnetwork']['eth_router'] + "\n"
				new_content += "static domain_name_servers=" + api_answer['newnetwork']['eth_network_domain'] + "\n"
				content = new_content.split('\n')
			tteller = 0
			new_content = ''

			if api_answer['newnetwork']['wlan_dhcp_fixed'] == 'dhcp':
				for row in content:
					if not (row == 'interface wlan0' or tteller == 1 or tteller == 2 or tteller == 3):
						if new_content != '':
							new_content += "\n"
						new_content += row
					else:
						tteller += 1
				content = new_content.split('\n')
			elif api_answer['newnetwork']['wlan_dhcp_fixed'] == 'static':
				for row in content:
					if not (row == 'interface wlan0' or tteller == 1 or tteller == 2 or tteller == 3):
						if new_content != '':
							new_content += "\n"
						new_content += row
					else:
						tteller += 1
				new_content += "interface wlan0\n"
				sstr = api_answer['newnetwork']['wlan_static_IP']
				if not '/' in sstr:
					sstr += "/24"
				new_content += "static ip_address=" + sstr + "\n"
				new_content += "static routers=" + api_answer['newnetwork']['wlan_router'] + "\n"
				new_content += "static domain_name_servers=" + api_answer['newnetwork']['wlan_network_domain'] + "\n"
				content = new_content.split('\n')
			tteller = 0

			new_content = ''
			for row in content:
				if new_content != '':
					new_content += "\n"
				new_content += row
			f = open('/etc/dhcpcd.conf', 'w')
			f.write(new_content)
			f.close()
		sts.add('newnetwork', api_answer['newnetwork']['id'])
		cf.check_update_config('last_newnetwork_job', api_answer['newnetwork']['id'])
		runteller = 0
	if 'userid' in api_answer:
		if cf.check_update_config('userid', api_answer['userid']) == 'updated':
			ffile = '/etc/hosts'
			os.system('sudo chmod 777 ' + ffile)
			f = open(ffile, 'r')
			sstr = ''
			for line in f:
				if line[:9] == '127.0.1.1':
					sstr += '127.0.1.1' + "\t" + api_answer['userid'] + "\n"
				else:
					sstr += line
			f = open(ffile, 'w')
			f.write(sstr)
			f.close()
			ffile = '/etc/hostname'
			f = open(ffile, 'w')
			f.write(api_answer['userid'])
			f.close()
		runteller = 0
	if 'id' in api_answer: 
		cf.check_update_config('id', api_answer['id'])
	if 'rpiclicommands' in api_answer: 
		cf.check_update_config('rpiclicommands', api_answer['rpiclicommands'])
	if 'reverse_ssh_server' in api_answer: 
		cf.check_update_config('reverse_ssh_server', api_answer['reverse_ssh_server'])
	if 'id_rsa_pub' in api_answer and os.path.isfile('/home/dietpi/.ssh/id_rsa.pub'):
		f = open('/home/dietpi/.ssh/id_rsa.pub','r')
		contents = f.read()
		sts.add('id_rsa_pub',0,contents.rstrip())

commands = cf.read('rpiclicommands')
# lets see if there is a command not yet done. We will perform the one with the lowest id but 
# larger than the job-id from the last job.
lowest_id = 0
while lowest_id < 99999999:
	lowest_id = 99999999
	for c in commands:
		if c['id'] < lowest_id and c['id'] > int('0' + str(cf.read('last_clicommand_job'))):
			lowest_id = c['id']
			lowest_command = c['sent']
	if lowest_id < 99999999:
		# command = lowest_command.split(' ')
		command = lowest_command
		print('cli:' + command)
		#ps = subprocess.run([command], capture_output=True, text=True).stdout
		os.system(command + ' > /tmp/output.txt')
		f = open('/tmp/output.txt', 'r')
		outputt = f.read()
		print(outputt)
		f.close()
		sts.add('clicommand',lowest_id, outputt[:499])
		cf.check_update_config('last_clicommand_job', lowest_id)
		runteller = 0

if not os.path.isfile('/home/dietpi/ssh_port') or int(ssm.comp_nr_only_dec) % 60 == now.minute or sysargv == 'test8':
	reverse_ssh_server = ourserver
	if cf.read('reverse_ssh_server') != '':
		reverse_ssh_server = cf.read('reverse_ssh_server')
	print('our server' + reverse_ssh_server +'x')
	if os.path.isfile('/home/dietpi/ipaddress'):
		f = open('/home/dietpi/ipaddress', 'r')
		sstr = f.read()
		f.close()
		sstr = sstr.rstrip()
	else:
		sstr = ''
	print('sstr:' + sstr +'x')
	if sstr != reverse_ssh_server and reverse_ssh_server != '':
		f = open('/home/dietpi/ipaddress', 'w+')
		f.write(reverse_ssh_server)
		f.close()


if cf.read('activation_code') != '':
	runteller = 0
else:
	runteller += 1
	f = open('/dev/shm/frequency', 'w+')
	f.write(str(int(runteller)))
	f.close()

print('m.py ' + now.strftime('%Y-%m-%d %H:%M'))
