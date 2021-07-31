from time import sleep
import os.path, time
import os
import datetime
import subprocess
import sys

def replaceline(ffile, oldsting, newstring):
  os.system('sudo chmod 777 ' + ffile)
  f = open(ffile, 'r')
  sstr = ''
  for line in f:
    sstr += line.replace(oldsting, newstring)
  f = open(ffile, 'w')
  f.write(sstr)
  f.close()

def writelog(sstr):
  now = datetime.datetime.now()
  f = open('/home/dietpi/l', 'a')
  f.write(now.strftime("%Y %m %d %H:%M ") + sstr + "\n")
  f.close()
  print (sstr)

def ossystem(sstr):
	os.system(sstr)
	writelog(sstr)

oursystem = 'django2'

if True:
	f = open("/bin/l", 'w')
	f.write('ls -l $1')
	f.close()
	ossystem('sudo chmod 777 /bin/l')
	f = open("/bin/s", 'w')
	f.write('sudo service apache2 restart')
	f.close()
	ossystem('sudo chmod 777 /bin/s')
if True:
	f = open("/home/dietpi/log.txt", 'w')
	f.write('New system.')
	f.close()

if True:

# source:
# https://pimylifeup.com/raspberry-pi-django/
	ossystem('sudo apt-get -y install nginx')
	ossystem('sudo apt-get -y install python3 python3-venv python3-pip')

if True:
	sstr = '''
server {
       listen 2020;

       server_name _;

         location /static/ {
                root /home/dietpi/pidjango;
               # add_header Cache-Control "public, max-age=86400" always;
        }
       location / {
                include proxy_params;
                proxy_pass http://unix:/home/dietpi/pidjango/gunicorn.sock;
        }
}

'''
	replaceline('/etc/apache2/sites-available/default',sstr)
	ossystem('mkdir -p /home/dietpi/pidjango/static')
	ossystem('mkdir -p /home/dietpi/pidjango/static/admin')
	ossystem('mkdir -p /home/dietpi/pidjango/static/admin/css')
	ossystem('mkdir -p /home/dietpi/pidjango/static/xx')
if False:
	ossystem('cd /home/dietpi/pidjango && python3 -m venv djenv')
	ossystem('cd /home/dietpi/pidjango && source djenv/bin/activate') # if manual: from here you get (djenv) on the command line left from the prompt.
	ossystem('cd /home/dietpi/pidjango && python3 -m pip install django gunicorn')

sstr = '''
cd /home/dietpi/pidjango && \
python3 -m venv djenv && \
# if manual: from here you get (djenv) on the command line left from the prompt.
source djenv/bin/activate && \
# next time try withour 3
python -m pip install django gunicorn && \

# werkt alleen met sudo ervoor
django-admin startproject pidjango . && \

python manage.py makemigrations && \
python manage.py migrate && \
python manage.py createsuperuser && \
DJANGO_SUPERUSER_PASSWORD=admin \
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=example@email.com \
./manage.py createsuperuser \
--no-input && \
#sudo cp /home/dietpi/pidjango/djenv/lib/python3.7/site-packages/django/contrib/admin/static/admin/css/base.css /home/dietpi/pidjango/static/admin/css && \
sudo chmod 777 * -R && \
# next line is to prevent that the database is readonly
sudo chmod 777 /home/dietpi/pidjango && \
systemctl restart nginx
'''
print (sstr)
f = open("/home/dietpi/s.sh", 'w')
f.write(sstr)
f.close()
ossystem('sudo chmod 777 /home/dietpi/s.sh')
ossystem('sudo /home/dietpi/s.sh')
if True:
	ossystem('sudo cp /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime')
	try:
		replaceline('/home/dietpi/pidjango/pidjango/setting.py','ALLOWED_HOSTS = []','ALLOWED_HOSTS = ["*"]')
		replaceline('/home/dietpi/pidjango/pidjango/setting.py','USE_L10N = True','USE_L10N = False')
		replaceline('/home/dietpi/pidjango/pidjango/setting.py','USE_TZ = True','USE_TZ = False')
		replaceline('/home/dietpi/pidjango/pidjango/setting.py',"TIME_ZONE = 'UTC'","TIME_ZONE = 'Europe/Amsterdam'")
		writelog('ALLOWED_HOSTS = ["*"]            DONE !')

		sstr = "\nDATETIME_FORMAT = 'Y-m-d H:i'\n"
		sstr += "SHORT_DATETIME_FORMAT = ['%Y-%m-%d H:%M']\n"

		f = open("/home/dietpi/pidjango/pidjango/setting.py", 'a')
		f.write(sstr)
		f.close()



	except:
		writelog('ALLOWED_HOSTS = ["*"] not set in setting.py')
	replaceline('/etc/hosts','raspberrypi',oursystem)
	replaceline('/etc/hostname','raspberrypi',oursystem)
	writelog('ready')
