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
	f = open('/home/pi/l', 'a')
	f.write(now.strftime("%Y %m %d %H:%M ") + sstr + "\n")
	f.close()
	print (sstr)

if True:
	f = open("/home/pi/log.txt", 'w')
	f.write('New system.')
	f.close()
	writelog('/home/pi/log.txt')
if True:
	os.system('sudo cp /usr/share/zoneinfo/Europe/Amsterdam /etc/localtime')
	writelog('time zone')
	f = open("/home/pi/config.txt", 'w')
	sstr = '{"reverse_ssh_server": "henk.waaromzomoeilijk.nl", "version":"00000"}'
	f.write(sstr)
	f.close()
	writelog('config.txt')
	f = open("/home/pi/ssh_port", 'w')
	f.write('12345')
	f.close()
	f = open("/home/pi/ipaddress", 'w')
	f.write('henk.waaromzomoeilijk.nl')
	f.close()
	f = open("/bin/l", 'w')
	f.write('ls -l $1')
	f.close()
	os.system('sudo chmod 777 /bin/l')
	writelog('/home/pi/ipaddress')
	sstr = "* * * * * sudo python3 /home/pi/m.py >/dev/null 2>&1 &"
	sstr += "\n" + '*/5 * * * * ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -fNTR $(cat "/home/pi/ssh_port"):localhost:80 remote@$(cat \"/home/pi/ipaddress\") -p 9212'
	sstr = "cat <(crontab -l) <(echo '"+sstr+"') | crontab -"
	subprocess.call(['bash', '-c', sstr])
	writelog('crontab')
