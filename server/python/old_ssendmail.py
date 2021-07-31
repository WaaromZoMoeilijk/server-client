import sys
import smtplib
from email.mime.text import MIMEText

sender = ''
receivers = 'wzc@waaromzomoeilijk.nl'
smtp_server = 'mail.waaromzomoeilijk.nl'
mailuser = ''
password = ""

message = "From: From WaaromZoMoeilijk <noreply@waaromzomoeilijk.nl>\n"
message += "To: <" + receivers + ">\n"
message += "WaaromZoCloud Notification\n\n"

server = smtplib.SMTP_SSL(smtp_server, 465)

server.ehlo()
server.login(mailuser, password)
server.sendmail(sender, receivers, message)
server.quit()
