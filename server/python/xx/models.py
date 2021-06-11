from django.db import models

# only make changes in xx/models.py

class Xuser(models.Model):
	name = models.CharField(max_length=50, null=True)
	userid  = models.CharField(max_length=12,blank=False, null=True)
	password = models.CharField(max_length=12,blank=True, null=True, help_text="at least 8 long, one capital, one special character")
	password2 = models.CharField(max_length=12,blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	new_email = models.EmailField(blank=True, null=True)
	activation_code = models.CharField(max_length=4,blank=True, null=True)
	activation_code_nw_email = models.CharField(max_length=12,blank=True, null=True)
	last_login = models.DateTimeField()
	created = models.DateTimeField(blank=True, auto_now_add=True)
	support_end_date = models.DateTimeField(blank=True,default='2021-05-22')
	last_updated = models.DateTimeField(blank=True)
	failed_logins = models.IntegerField(blank=True, default=0)
	ROLES = [
		('admin', 'admin'),
		('regular','regular'),
		]
	role = models.CharField(blank=True, max_length=12,choices=ROLES,default='regular')

	def __str__(self):
		return str(self.id) + ' ' + self.userid

	def get_menu(self):
		if self.role == 'admin':
			sstr = {'/xx/newrpi': 'new devices', '/xx/users': 'users', '/xx/settings':'settings', '/xx/clicommands':'cli commands'}
		else:
			sstr = {'/xx/xrpis': 'my devices', '/xx/xnewrpi': 'new device'}
		sstr['/xx/myaccount'] = 'my account'
		sstr['/xx/password'] = 'reset password'
		sstr['/'] = 'logout'
		return sstr

class CliCommand(models.Model):
	code = models.CharField(max_length=18)
	command = models.CharField(max_length=500)
	remark = models.CharField(max_length=500,blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(blank=True, null=True)

class NewNetwork(models.Model):
	rpi = models.ForeignKey('Rpi', on_delete=models.CASCADE)
	newssid = models.CharField(max_length=36,blank=True, null=True)
	psk = models.CharField(max_length=36,blank=True, null=True)
	DHCP_FIXED = [
	('dhcp', 'dhcp'),
	('fixed','fixed'),
	]
	wlan_dhcp_fixed = models.CharField(max_length=5,choices=DHCP_FIXED,default='dhcp')
	wlan_static_IP = models.CharField(max_length=36,blank=True, null=True)
	wlan_router = models.CharField(max_length=36,blank=True, null=True)
	wlan_network_domain = models.CharField(max_length=36,blank=True, null=True)
	eth_dhcp_fixed = models.CharField(max_length=5,choices=DHCP_FIXED,default='dhcp')
	eth_static_IP = models.CharField(max_length=36,blank=True, null=True)
	eth_router = models.CharField(max_length=36,blank=True, null=True)
	eth_network_domain = models.CharField(max_length=36,blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	# if last_updated filled, it is done in the rpi
	last_updated = models.DateTimeField(blank=True, null=True)

class NewRpi(models.Model):
	computernr = models.CharField(max_length=24)
	activation_code = models.CharField(max_length=12,blank=True, null=True)
	version = models.CharField(max_length=5,default='00000')
	created = models.DateTimeField(auto_now_add=True)
	last_seen = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id) + ' ' + self.computernr + ' ' + str(self.created)[:16]

class Rpi(models.Model):
	xuser = models.ForeignKey('Xuser', on_delete=models.CASCADE)
	computernr = models.CharField(max_length=24)
	version = models.CharField(max_length=5,default='00000')
	wifiAvailableNetworks = models.CharField(max_length=256,blank=True, null=True)
	wifiCurrentNetwork = models.CharField(max_length=36,blank=True, null=True)
	wifiKnownNetworks = models.CharField(max_length=256,blank=True, null=True)
	ipAddressWlan = models.CharField(max_length=36,blank=True, null=True)
	ipAddressEth = models.CharField(max_length=36,blank=True, null=True)
	# remove next
	ipAddressWAN = models.CharField(max_length=36,blank=True, null=True)
	ping_response_time = models.CharField(max_length=50,blank=True, null=True) # server/client
	sd_card = models.CharField(max_length=36,blank=True, null=True) # size and free space
	id_rsa_pub = models.CharField(max_length=400,default='',blank=True)
	last_reboot = models.DateTimeField(max_length=24,blank=True, null=True)
	STATI = [
	('active','active'),
	('blocked','blocked'),
	]
	status = models.CharField(max_length=12,choices=STATI,default='initial')
	created = models.DateTimeField()
	last_seen = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.id) + ' ' + self.computernr
	def asdict(self):
		respons = {}
		respons['id'] = self.id
		respons['computernr'] = self.computernr
		respons['version'] = self.version
		respons['wifiAvailableNetworks'] = self.wifiAvailableNetworks
		respons['wifiCurrentNetwork'] = self.wifiCurrentNetwork
		respons['wifiKnownNetworks'] = self.wifiKnownNetworks
		respons['ipAddressWlan'] = self.ipAddressWlan
		respons['ipAddressEth'] = self.ipAddressEth
		respons['ipAddressWAN'] = self.ipAddressWAN
		respons['ping_response_time'] = self.ping_response_time
		respons['sd_card'] = self.sd_card
		respons['id_rsa_pub'] = self.id_rsa_pub
		respons['last_reboot'] = self.last_reboot
		respons['created'] = self.created
		respons['last_seen'] = self.last_seen
		respons['userid'] = self.xuser.userid
		return respons

class RpiLogline(models.Model):
	rpi = models.ForeignKey('Rpi', on_delete=models.CASCADE)
	text = models.CharField(max_length=500)
	created = models.DateTimeField(auto_now_add=True)

class RpiCliCommand(models.Model):
	rpi = models.ForeignKey('Rpi', on_delete=models.CASCADE)
	sent = models.CharField(max_length=500)
	response = models.CharField(max_length=500,blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(blank=True, null=True)

class Settings(models.Model):
	sender = models.CharField(max_length=66,blank=True, null=True)
	smtp_server = models.CharField(max_length=66,blank=True, null=True)
	message_new_user = models.CharField(max_length=600,blank=True, null=True)
	free_period_in_months = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return str(self.id)
