# source djenv/bin/activate
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
#, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import time, random, json
#from xx.models import Xuser, Customer, Invoice, InvoiceLine, NewNetwork, Rpi, RpiLogline, RpiCliCommand, NewRpi
from xx.models import *
from .forms import XuserForm, MyAccountForm, NewNetworkForm, RpiForm, RegisterForm, SettingsForm, XnewRpiForm
#from .forms import *
import datetime
from django.views import View
from django.utils.decorators import method_decorator

def has_content(data, sstr):
	if sstr in data:
		if data[sstr] == None or data[sstr] == '':
			return False
		else:
			return True
	else:
		return False

def sendmail(name, email,actcode):
	import smtplib
	from email.mime.text import MIMEText
	settings = Settings.objects.get(id=1)
	sender = settings.sender
	smtp_server = settings.smtp_server
	message = "From: From HelloWZM " + sender + "\nTo: " + name + " <" + email + ">\nSubject: Activation Code WaaromZoMoeilijk:\n"
	message += settings.message_new_user
	message = message.replace('aaa',actcode + ' ')
	message = message.replace('eee',email)
	message = message.replace('nnn',name)
	message = message.replace('sss',sender)
	smtpObj = smtplib.SMTP(smtp_server, 25)
	smtpObj.sendmail(sender, email, message)
	#return message + 'X' + smtp_server


def table_bg_color(sstr):
	bgcolor = 'ffffff'
	for s in sstr:
		if bgcolor == 'ffffff':
			bgcolor = 'eeeeee'
		else:
			bgcolor = 'ffffff'
		s.bgcolor = bgcolor
	return sstr

def activate(request, a):
	context = {}
	if True:
		xuser = Xuser.objects.get(userid=a[4:], activation_code=a[:4])
		xuser.activation_code = ''
		xuser.last_updated = timezone.now()
		settings = Settings.objects.get(id=1)
		xuser.support_end_date = timezone.now() + timezone.timedelta(days=31*settings.free_period_in_months)
		xuser.save()
		context['errorr'] = 'Thanks. You can now use your account.'
		return render(request, 'activate.html',context)
	else:
		context['errorr'] = 'Contact support.'
		return render(request, 'activate.html',context)

@method_decorator(csrf_exempt, name='dispatch')
class Api(View):
	def post(self, request):
		data = json.loads(request.body.decode("utf-8"))
		status = ''
		respons = {}
		try:
			computernr = data['computernr']
			version = data['version']
		except:
			return JsonResponse({'error': 'a0'}, status=401)
		try:
			rpi = Rpi.objects.get(computernr=computernr)
			status = 'known device'
		except:
			try:
				newrpi = NewRpi.objects.get(computernr=computernr)
				status = 'waiting activation'
			except:
				status = 'brandnew'
		respons['status'] = status
		if status == 'brandnew':
			newid = None
			# we look for a free id.
			tteller = 0
			while tteller < 22:
				tteller += 1
				try:
					newid = NewRpi.objects.get(pk=tteller)
				except:
					newid = tteller
					tteller = 9999
			newrpi = NewRpi()
			newrpi.id = newid
			newrpi.computernr = computernr
			numbers = '0123456789'
			activation_code = ''
			while len(activation_code) < 6:
				activation_code += numbers[random.randint(0,9)]
			newrpi.activation_code = activation_code
			newrpi.version = version
			newrpi.created = timezone.now()
			newrpi.last_seen = timezone.now()
			newrpi.save()
			respons['id'] = newrpi.id
			respons['activation_code'] = newrpi.activation_code
			respons['status'] = 'a1'
			return JsonResponse(respons)
		elif status == 'waiting activation':
			newrpi.last_seen = timezone.now()
			newrpi.save()
			respons['id'] = newrpi.id
			respons['activation_code'] = newrpi.activation_code
			respons['status'] = 'a2'
			return JsonResponse(respons)
		elif status == 'known device':
			rpi.last_seen = timezone.now()
			rpi.version = version
			if has_content(data, 'wifiAvailableNetworks'):
				rpi.wifiAvailableNetworks = data['wifiAvailableNetworks']
			if has_content(data, 'wifiCurrentNetwork'):
				rpi.wifiCurrentNetwork = data['wifiCurrentNetwork']
			if has_content(data, 'wifiKnownNetworks'):
				rpi.wifiKnownNetworks = data['wifiKnownNetworks']
			if has_content(data, 'ipAddressWlan'):
				rpi.ipAddressWlan = data['ipAddressWlan']
			if has_content(data, 'ipAddressEth'):
				rpi.ipAddressEth = data['ipAddressEth']
			if has_content(data, 'sd_card'):
				rpi.sd_card = data['sd_card']
			if has_content(data, 'last_reboot'):
				rpi.last_reboot = '20' + data['last_reboot']
			if has_content(data, 'ping_response_time'):
				rpi.ping_response_time = data['ping_response_time']
			rpi.save()
			rpilogline = RpiLogline()
			rpilogline.rpi = rpi
			rpilogline.text = json.dumps(data)
			rpilogline.save()
			if 'sendtoserver' in data:
				rpiclicommands = data['sendtoserver']
				for r in rpiclicommands:
					if r['jobname'] == 'newnetwork':
	#					newnetwork = NewNetwork.objects.get(pk=r['id'])
						newnetwork = NewNetwork.objects.get(id=r['id'])
						newnetwork.last_updated = timezone.now()
						newnetwork.save()
					if r['jobname'] == 'clicommand':
						rpiclicommand = RpiCliCommand.objects.get(id=r['id'])
						rpiclicommand.response = r['response']
						rpiclicommand.last_updated = timezone.now()
						rpiclicommand.save()
					context['message'] = 'data saved'
			respons['id'] = rpi.id
			respons['userid'] = rpi.xuser.userid
			respons['status'] = 'a9'
			sstr = RpiCliCommand.objects.filter(rpi_id=rpi.id).filter(last_updated=None)
			clicommands = []
			for s in sstr:
				clicommands.append({"id": s.id, "sent": s.sent})
			if len(clicommands) > 0:
				respons['rpiclicommands'] = clicommands
			sstr = NewNetwork.objects.filter(rpi_id=rpi.id).filter(last_updated=None).first()
			if sstr != None:
				newnetwork = {}
				newnetwork['id'] = sstr.id
				newnetwork['newssid'] = sstr.newssid
				newnetwork['psk'] = sstr.psk
				newnetwork['wlan_dhcp_fixed'] = sstr.wlan_dhcp_fixed
				newnetwork['wlan_static_IP'] = sstr.wlan_static_IP
				newnetwork['wlan_router'] = sstr.wlan_router
				newnetwork['wlan_network_domain'] = sstr.wlan_network_domain
				newnetwork['eth_dhcp_fixed'] = sstr.eth_dhcp_fixed
				newnetwork['eth_static_IP'] = sstr.eth_static_IP
				newnetwork['eth_router'] = sstr.eth_router
				newnetwork['eth_network_domain'] = sstr.eth_network_domain
				respons['newnetwork'] = newnetwork
			respons['iid'] = rpi.id
			return JsonResponse(respons)

def check_user(request):
	try:
		userid = request.session['userid']
	except:
		userid = ''
	if userid == '':
		rs = {'message': 'Illegal request.', 'loggedin': False}
	elif not 'lastactive' in request.session:
		rs = {'message': 'Please login.', 'loggedin': False}
	elif request.session['lastactive'] + 600 < time.time():
		rs = {'message': 'Session expired.', 'loggedin': False}
	else:
		rs = {'message': 'Your logged in as ' + userid, 'loggedin': True, 'userid': userid}
		request.session['lastactive'] = time.time()
	try:
		last_post = request.session['last_post']
	except:
		last_post = ''
	if last_post == json.dumps(request.POST):
		rs['canprocess'] = 'n'
	else:
		rs['canprocess'] = 'y'
		request.session['last_post'] = json.dumps(request.POST)
	return rs

#@csrf_exempt
def checklogin(request):
	#if True:
	try:
		xuser = Xuser.objects.get(userid=request.POST['userid'])
		if xuser.failed_logins > 4:
			xuser.failed_logins = 1 + xuser.failed_logins
			xuser.save()
			context = {'message': 'Too many failed logins'}
			return render(request, 'login.html', context)
		if xuser.activation_code != '' and xuser.activation_code != None:
			xuser.failed_logins = 1 + xuser.failed_logins
			xuser.save()
			context = {'message': 'Account not activated'}
			return render(request, 'login.html', context)
		elif xuser.password == request.POST['password']:
			request.session['lastactive'] = time.time()
			request.session['userid'] = request.POST['userid']
			context = {'message': 'Your logged in as ' + request.POST['userid']}
			xuser.last_login = timezone.now()
			xuser.failed_logins = 0
			xuser.save()
			context['menu'] = xuser.get_menu()
			context['content'] = 'Latest news: we just sold rpi number 250 !.'
			return render(request, 'home.html', context)
		else:
			xuser.failed_logins = 1 + xuser.failed_logins
			xuser.save()
			context = {'message': 'Wrong password'}
			return render(request, 'login.html', context)
	#else:
	except:
		context = {'message': 'Login or register.'}
		return render(request, 'login.html', context)

#@csrf_exempt
def home(request):
	context = check_user(request)
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	else:
		context['menu'] = xuser.get_menu()
		context['content'] = '<h2>hijklm</h2>'
		return render(request, 'home.html',context)

#@csrf_exempt
def myaccount(request):
	context = check_user(request)
#	form = MyAccountForm()
	#sstr = f.is_valid()
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	if request.method == 'POST':
		xuser = Xuser.objects.get(userid=request.session['userid'])
		form = MyAccountForm(data=request.POST)
		#form.is_valid()
		if form.is_valid(): # the 'not' cannot be good.
#	#elif True:
			xuser.name = form.cleaned_data['name']
			xuser.email = form.cleaned_data['email']
			xuser.password = form.cleaned_data['password']
			xuser.last_updated = timezone.now()
			xuser.save()
			context['form'] = MyAccountForm(initial=xuser.__dict__)
			context['message'] = 'data saved'
		else:
			#xuser = bbb
			xuser = Xuser.objects.get(userid=request.session['userid'])
			xuser.name = 'B' + form.cleaned_data['name']
			#context['form'] = XuserForm(initial=xuser.__dict__)
			#context['form'] = XuserForm(xuser.__dict__)
			context['form'] = form
			context['form'] = MyAccountForm(initial=xuser.__dict__)
			context['message'] = 'please repair invalid data'
		context['menu'] = xuser.get_menu()
		context['userid'] = xuser.userid
		#context['created'] = xuser.created.strftime("%Y-%m-%d %H:%M")
		return render(request, 'myaccount.html',context)
		#return HttpResponse("Data submitted successfully")
	else:
		xuser = Xuser.objects.get(userid=request.session['userid'])
		#context = {}
		context['menu'] = xuser.get_menu()
		context['userid'] = xuser.userid
		#context['created'] = xuser.created.strftime("%Y-%m-%d %H:%M")
		context['form'] = MyAccountForm(initial=xuser.__dict__)
		return render(request, 'myaccount.html',context)

def newnetworkedit(request):
	context = check_user(request)
	xuser = Xuser.objects.get(userid=request.session['userid'])
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	else:
	#elif request.method == 'POST':
		context['xxid'] = request.session['id_rpi']
		context['breadcrumb'] = {'user': request.session['id_user'], 'rpi': request.session['id_rpi']}
		context['menu'] = xuser.get_menu()
		context['form'] = NewNetworkForm()
		#context['newnetworks'] = NewNetwork.objects.filter(xuser=xuser.id).order_by('name')
		return render(request, 'newnetworkedit.html',context)

def newnetworks(request):
	context = check_user(request)
	context['breadcrumb'] = {'user': request.session['id_user'], 'rpi': request.session['id_rpi']}
	xuser = Xuser.objects.get(userid=request.session['userid'])
	context['menu'] = xuser.get_menu()
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	elif request.method == 'POST':
		id = int(request.session['id_rpi'])
		try:
			coming_from = request.POST['coming_from']
		except:
			coming_from = ''
		if coming_from == 'newnetwork' and context['canprocess'] == 'y':
			form = NewNetworkForm(request.POST)
			if form.is_valid():
				newnetwork = NewNetwork()
				newnetwork.rpi_id = id
				newnetwork.newssid = form.cleaned_data['newssid']
				newnetwork.psk = form.cleaned_data['psk']
				newnetwork.wlan_dhcp_fixed = form.cleaned_data['wlan_dhcp_fixed']
				newnetwork.wlan_static_IP = form.cleaned_data['wlan_static_IP']
				newnetwork.wlan_router = form.cleaned_data['wlan_router']
				newnetwork.wlan_network_domain = form.cleaned_data['wlan_network_domain']
				newnetwork.eth_dhcp_fixed = form.cleaned_data['eth_dhcp_fixed']
				newnetwork.eth_static_IP = form.cleaned_data['eth_static_IP']
				newnetwork.eth_router = form.cleaned_data['eth_router']
				newnetwork.eth_network_domain = form.cleaned_data['eth_network_domain']
				newnetwork.created = timezone.now()
				newnetwork.save()
				context['message'] = 'data saved'
			else:
				context['form'] = form
				return render(request, 'newnetworkedit.html',context)
	else:
		context['form'] = NewNetworkForm()
		return render(request, 'newnetworks.html',context)

	context['xxid'] = id
	context['newnetworks'] = table_bg_color(NewNetwork.objects.filter(rpi=id).order_by('-created'))
	return render(request, 'newnetworks.html',context)
	#return HttpResponseRedirect(request.path)

def register(request):
	context = {}
	if 'name' in request.POST:
		post_is_filled = True
		userid_taken = Xuser.objects.filter(userid=request.POST['userid'].lower()).count()
		form = RegisterForm(request.POST)
		form_is_valid = form.is_valid()
	else:
		form_is_valid = False
		post_is_filled = False
		form = RegisterForm()
	#if not ('name' in request.POST and 'userid' in request.POST and request.POST['name'] == '') and request.POST['userid'] == '':
	#	context['errorr'] = 'Parameters missing'
	if not post_is_filled:
		context['errorr'] = ''
#	elif request.POST['password'] != request.POST['password2']:
#		context['errorr'] = 'Passwords are not the same'
	elif userid_taken > 0:
		free_id = Xuser.objects.order_by('-id').first()
		free_id = request.POST['userid'] + str(free_id.id)
		context['errorr'] = 'Userid taken already. Try another, for instance: ' + free_id
	elif form_is_valid:
		xuser = Xuser()
		xuser.name = form.cleaned_data['name']
		xuser.userid = form.cleaned_data['userid'].lower()
		xuser.password = form.cleaned_data['password']
		xuser.email = form.cleaned_data['email']
		sstr = int(datetime.datetime.now().strftime('%s')) % 9377
		xuser.activation_code = "{:04d}".format(sstr)
		xuser.created = timezone.now()
		xuser.role = 'regular'
		xuser.failed_logins = 0
		xuser.last_updated = timezone.now()
		xuser.last_login = timezone.now()
		xuser.save()
		sendmail(xuser.name, xuser.email, xuser.activation_code + xuser.userid)
		context['email'] = form.cleaned_data['email']
		context['errorr'] = ''
		return render(request, 'register_thanks.html',context)
	context['form'] = form
	return render(request, 'register.html',context)

def register_thanks(request):
		return render(request, 'register_thanks.html')

def rpiclicommand(request):
	id = request.session['id_rpi']
	context = check_user(request)
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	else:
		xuser = Xuser.objects.get(userid=request.session['userid'])
		context['menu'] = xuser.get_menu()
		context['breadcrumb'] = {'user': request.session['id_user'], 'rpi': request.session['id_rpi']}
		context['rpiclicommands'] = table_bg_color(RpiCliCommand.objects.filter(rpi=id).order_by('-created'))
		return render(request, 'rpiclicommand.html',context)

def rpiedit(request, id=None):
	context = check_user(request)
	xuser = Xuser.objects.get(userid=request.session['userid'])
	try: # invoice_id can arrive in <int:id> or POST['xxid']
		id = int(id)
	except:
		id = None
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	elif id == None:
		context['menu'] = xuser.get_menu()
		return render(request, 'home.html',context)
	request.session['id_rpi'] = id
	context = {}
	context['message'] = 'Cant find an device'
	context['menu'] = xuser.get_menu()
	#context['breadcrum'] = 'userr:' + str(request.session['rpi']) + 'X' + str(request.session['user']) + 'X'
	#context['breadcrum'] = [{'user': request.session['user']}, {'rpi': request.session['rpi']}]
	context['breadcrumb'] = {'user': request.session['id_user'], 'rpi': request.session['id_rpi']}
	context['xxid'] = id
	rpi = Rpi.objects.get(pk=id)
	sstr = rpi.__dict__
	context['form'] = RpiForm(initial=sstr)
	return render(request, 'rpiedit.html',context)

def rpilogline(request):
	id = request.session['id_rpi']
	context = check_user(request)
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	else:
		xuser = Xuser.objects.get(userid=request.session['userid'])
		context['menu'] = xuser.get_menu()
		context['breadcrumb'] = {'user': request.session['id_user'], 'rpi': request.session['id_rpi']}
		context['rpiloglines'] = table_bg_color(RpiLogline.objects.filter(rpi=id).order_by('-created'))
		return render(request, 'rpilogline.html',context)

def settings(request):
	context = check_user(request)
	xuser = Xuser.objects.get(userid=request.session['userid'])
	context['menu'] = xuser.get_menu()
	try:
		settings = Settings.objects.get(id=1)
		context['form'] = SettingsForm(initial=settings.__dict__)
	except:
		context['form'] = SettingsForm()
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	if request.method == 'POST':
		form = SettingsForm(data=request.POST)
		settings.sender = request.POST['sender']
		settings.smtp_server = request.POST['smtp_server']
		settings.message_new_user = request.POST['message_new_user']
		#try:
		settings.free_period_in_months = int(request.POST['free_period_in_months'])
		#except:
			#void
		settings.save()
		try:
			sstr = sendmail('Test Name', xuser.email,'x9999' + xuser.userid)
			context['message'] = 'data saved & message sent'
		except:
			context['message'] = 'data saved & no message'
	return render(request, 'settings.html',context)

def newrpi(request):
	context = check_user(request)
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	else:
		xuser = Xuser.objects.get(userid=request.session['userid'])
		context['menu'] = xuser.get_menu()
		context['newrpis'] = NewRpi.objects.all().order_by('created')
		return render(request, 'newrpi.html',context)

def useredit(request, id=None):
	context = check_user(request)
	xuser = Xuser.objects.get(userid=request.session['userid'])
	#request.session['id_user'] = xuser.id
	if id == None:
		id = request.session['id_user']
	else:
		request.session['id_user'] = id
	user = Xuser.objects.get(pk=id)
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	elif request.method == 'POST':
		# save data existing user
		if int(request.POST['addnewrpi']) == 0:
			user.name = request.POST['name']
			if len(request.POST['password']) > 0:
				user.password = request.POST['password']
			user.email = request.POST['email']
			user.role = request.POST['role']
			user.last_updated = timezone.now()
			user.failed_logins = int(request.POST['failed_logins'])
			user.save()
		else:
			# add device to this user
			newrpi_id = int(request.POST['addnewrpi'])
			newrpi = NewRpi.objects.get(pk=newrpi_id)
			rpi = Rpi()
			rpi.id = None
			rpi.xuser_id = id
			rpi.computernr = newrpi.computernr
			rpi.version = newrpi.version
			rpi.status = 'active'
			rpi.created = newrpi.created
			rpi.last_seen = newrpi.last_seen
			rpi.save()
			newrpi.delete()
		context['message'] = 'data saved'
	elif id != None:
		# display data existing user
		user = Xuser.objects.get(pk=id)
	context['menu'] = xuser.get_menu()
	context['xxid'] = id
	context['form'] = XuserForm(initial=user.__dict__)
	context['rpis'] = table_bg_color(user.rpi_set.all())
	context['newrpis'] =NewRpi.objects.all()
	return render(request, 'useredit.html',context)

def users(request):
	context = check_user(request)
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	else:
		xuser = Xuser.objects.get(userid=request.session['userid'])
		context['menu'] = xuser.get_menu()
		bgcolor = 'ffffff'
		#context['users'] = Xuser.objects.filter(xuser=id).order_by('name')
		context['users'] = table_bg_color(Xuser.objects.order_by('name'))
		return render(request, 'users.html',context)

def xnewrpi(request):
	context = check_user(request)
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	else:
		xuser = Xuser.objects.get(userid=request.session['userid'])
		context['form'] = XnewRpiForm()
		context['menu'] = xuser.get_menu()
		context['userid'] = xuser.userid

		if request.method == 'POST':
			form = XnewRpiForm(data=request.POST)
			if form.is_valid():
				#form = XnewRpiForm(data=request.POST)
				newrpi = NewRpi.objects.get(computernr=form.cleaned_data['computernr'], activation_code=form.cleaned_data['activation_code'])
				rpi = Rpi()
				rpi.id = None
				rpi.xuser_id = xuser.id
				rpi.computernr = newrpi.computernr
				rpi.version = newrpi.version
				rpi.status = 'active'
				rpi.created = newrpi.created
				rpi.last_seen = newrpi.last_seen
				rpi.save()
				request.session['id_rpi'] = rpi.id
				newrpi.delete()
				context['message'] = 'data saved'
			else:
	#			form = XnewRpiForm(data=request.POST)
				context['message'] = 'Check entered data'
				context['form'] = XnewRpiForm(request.POST)
		return render(request, 'xnewrpi.html',context)

def xrpis(request):
	context = check_user(request)
	if not context['loggedin']:
		return HttpResponseRedirect('/../index.html')
	else:
		xuser = Xuser.objects.get(userid=request.session['userid'])
		context['menu'] = xuser.get_menu()
		context['newrpis'] = table_bg_color(Rpi.objects.filter(xuser_id=xuser.id).order_by('created'))
		return render(request, 'xrpis.html',context)
