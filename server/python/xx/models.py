from django.db import models

# only make changes in xx/models.py

class Xuser(models.Model):
	name = models.CharField(max_length=50, null=True)
	userid  = models.CharField(max_length=12,blank=False, null=True)
	password = models.CharField(max_length=12,blank=False, null=True)
	email = models.EmailField(blank=True, null=True)
	new_email = models.EmailField(blank=True, null=True)
	activation_code = models.CharField(max_length=4,blank=True, null=True)
	activation_code_nw_email = models.CharField(max_length=12,blank=True, null=True)
	last_login = models.DateTimeField()
	created = models.DateTimeField(blank=True, auto_now_add=True)
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
#		sstr = {'/xx/newrpi': 'new devices', '/xx/users': 'users', '/xx/settings':'settings-niet klaar', '/xx/myaccount':'my account', '/':'logout'}
		if self.role == 'admin':
			sstr = {'/xx/newrpi': 'new devices', '/xx/users': 'users', '/xx/settings':'settings', '/xx/myaccount':'my account', '/':'logout'}
		else:
			sstr = {'/xx/xrpis': 'my devices', '/xx/xnewrpi': 'new device', '/xx/myaccount':'my account', '/':'logout'}
		return sstr

class Customer(models.Model):
	xuser = models.ForeignKey('Xuser', on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	address1 = models.CharField(max_length=50,blank=True)
	address2 = models.CharField(max_length=50,blank=True)
	address3 = models.CharField(max_length=50,blank=True)
	zipcode = models.CharField(max_length=10,blank=True)
	city = models.CharField(max_length=50,blank=True)
	COUNTRIES = [
		('nl', 'Netherlands'),
		('be','Belgium'),
		('ae','United Arabic Emirates'),
		('uk', 'United Kingdom'),
		('us', 'United States'),
		]
	country = models.CharField(max_length=2,choices=COUNTRIES,default='nl')
	email = models.EmailField(max_length=50,blank=True)
	btw_number = models.CharField(max_length=50,blank=True)
	coc_number = models.CharField(max_length=50,blank=True)
	language = models.CharField(max_length=2,choices=[('nl', 'Dutch'),('en', 'English')])
	created = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

class Invoice(models.Model):
	customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	STATI = [('initial', 'initial'),('sent','sent'),('paid','paid'),('canceled','canceled'),]
	status = models.CharField(max_length=10,choices=STATI,default='initial')
	bill_number = models.IntegerField(blank=True, null=True)
	sent_date = models.DateTimeField(blank=True, null=True)
	paid_date = models.DateTimeField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

class InvoiceLine(models.Model):
	invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE)
	name = models.CharField(max_length=500)
	amount = models.FloatField()
	btw = models.FloatField(choices=[(0, '0'),(21, '21')],default=0)

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

	def __str__(self):
		return str(self.id)
