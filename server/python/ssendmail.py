import os
import sys
import smtplib
import datetime
from email.mime.text import MIMEText

verslag = ''
sstr = datetime.datetime.now()
verslag = sstr.strftime('%Y-%m-%d %H:%M') + "\n"

message_body = '''
Hi nnn,\n\nWelcome at WaaromZoMoeilijk\n\n
To activate your account, please click this link:\n\n
https://wzc.waaromzomoeilijk.nl/activate/aaa\n\n
Many Regards,\nStaff WaaromZoMoeilijk.nl
'''

name = sys.argv[1]
receivers = sys.argv[2]
actcode = sys.argv[3]
verslag += "n:"+ name + ',r:' + receivers + ',a:' + actcode + "\n"

sender = 'wzc@waaromzomoeilijk.nl'
smtp_server = 'mail.waaromzomoeilijk.nl'
mailuser = 'wzc@waaromzomoeilijk.nl'
password = ""

message = "From: From WaaromZoMoeilijk <noreply@waaromzomoeilijk.nl>\n"
message += "To: To " + name + " <" + receivers + ">\n"
message += "Subject: Activation WaaromZoCloud\n\n"
message += message_body

message = message.replace('aaa',actcode + ' ')
#message = message.replace('eee',email)
message = message.replace('nnn',name)
#message = message.replace('sss',sender)

try:
	server = smtplib.SMTP_SSL(smtp_server, 465)
	server.ehlo()
	server.login(mailuser, password)
	server.sendmail(sender, receivers, message)
	server.quit()
	verslag += "gelukt\n"
except:
	verslag += "something wrong\n"
if os.path.isfile('/dev/shm/verslag.txt'):
	f = open('/dev/shm/verslag.txt','r')
	contents =f.read()
else:
	contents = ''
f = open('/dev/shm/verslag.txt','w')
f.write(verslag + contents)
f.close()

