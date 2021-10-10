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

def ossystem(sstr):
	os.system(sstr)
	writelog(sstr)

def writelog(sstr):
	now = datetime.datetime.now()
	f = open('/home/dietpi/l', 'a')
	f.write(now.strftime("%Y %m %d %H:%M ") + sstr + "\n")
	f.close()
	print (sstr)

if True:
	f = open("/home/dietpi/log.txt", 'w')
	f.write('New system.')
	f.close()
	writelog('/home/dietpi/log.txt')
if True:
	f = open("/home/dietpi/config.txt", 'w')
	sstr = '{"reverse_ssh_server": "wzc.waaromzomoeilijk.nl", "version":"00000"}'
	f.write(sstr)
	f.close()
	writelog('config.txt')
	f = open("/home/dietpi/ssh_port", 'w')
	f.write("$(shuf -i10000-64000 -n1)")
	f.close()
	f = open("/home/dietpi/ipaddress", 'w')
	f.write('wzc.waaromzomoeilijk.nl')
	f.close()
	f = open("/bin/l", 'w')
	f.write('ls -l $1')
	f.close()
	os.system('sudo chmod 777 /bin/l')
	writelog('/home/dietpi/ipaddress')
	sstr = "* * * * * /usr/bin/sudo /usr/bin/python3 /home/dietpi/m.py >/dev/null 2>&1 &"
	sstr += "\n" + '* * * * * /bin/bash /var/opt/server-client/client/scripts/tunnel_check.sh'
	sstr = "cat <(crontab -l) <(echo '"+sstr+"') | crontab -"
	subprocess.call(['bash', '-c', sstr])
	writelog('crontab')
