from time import sleep
import os.path, time
import os
import datetime
import subprocess
import sys
import json
import requests
from ffunctions import *
import pygame

BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = ( 255, 0, 0)

try:
	pygame.init()
	pygame.mouse.set_visible(0)
	screen = pygame.display.set_mode((0,0),pygame.RESIZABLE)
	myfont = pygame.font.SysFont("Comic Sans MS", 50)
	bg = pygame.image.load("/home/dietpi/bg.jpg")
	display_attached = True
except:
	display_attached = False

tteller = 0
try:
	sysargv = sys.argv[1]
except:
	sysargv = ''

ssm = system_info()

while True:
	try:
		cf = configtxt()
	except:
		sstr = 'do nothing'
	if display_attached:
		if cf.read('activation_code') == '':
			lable_id = 'Username:'
			lable_act_code = ''
		else:
			lable_id = 'Temporary ID: '
			lable_act_code = 'Activation code: '
		screen.blit(bg, (0, 0))
	#	screen.fill((0,0,0))
		label = myfont.render(lable_id, 1, WHITE)
		screen.blit(label, (50, 50))
		label = myfont.render(str(cf.read('userid')), 1, GREEN)
		screen.blit(label, (500, 50))

		label = myfont.render("Device ID:", 1, WHITE)
		screen.blit(label, (50, 100))
		label = myfont.render(str(ssm.computernr), 1, GREEN)
		screen.blit(label, (500, 100))

		label = myfont.render("Wifi IP:", 1, WHITE)
		screen.blit(label, (50, 200))
		label = myfont.render(str(ssm.wlanIPaddress), 1, GREEN)
		screen.blit(label, (500, 200))

		label = myfont.render("LAN IP:", 1, WHITE)
		screen.blit(label, (50, 150))
		label = myfont.render(str(ssm.ethIPaddress), 1, GREEN)
		screen.blit(label, (500, 150))
		if cf.read('activation_code') == '':
			label = myfont.render("LAN url:", 1, WHITE) 
			screen.blit(label, (50, 250))
			label = myfont.render(str(cf.read('userid')), 1, GREEN)
			screen.blit(label, (400, 250))
			label = myfont.render(".local", 1, GREEN)
			screen.blit(label, (500, 250))
			label = myfont.render("Remote url:", 1, WHITE)
			screen.blit(label, (50, 300))
			label = myfont.render(str(cf.read('userid')), 1, GREEN)
			screen.blit(label, (400, 300))
			label = myfont.render(".waaromzomoeilijk.nl", 1, GREEN)
			screen.blit(label, (500, 300))
			label = myfont.render("Storage:", 1, WHITE)
			screen.blit(label, (50, 350))
			label = myfont.render(str(ssm.sd_info), 1, GREEN)
			screen.blit(label, (500, 350))
			label = myfont.render("Reverse SSH Port:", 1, WHITE)
			screen.blit(label, (50, 400))
			label = myfont.render(str(cf.read('ssh_port')), 1, GREEN)
			screen.blit(label, (500, 400))
		if cf.read('activation_code') != '':
			label = myfont.render(lable_act_code, 1, WHITE)
			screen.blit(label, (50, 400))
			label = myfont.render(cf.read('activation_code'), 1, GREEN)
			screen.blit(label, (500, 400))
		if cf.read('activation_code') != '':
			label = myfont.render("Please register:", 1, WHITE)
			screen.blit(label, (50, 450))
			label = myfont.render("wzc.waaromzomoeilijk.nl", 1, GREEN)
			screen.blit(label, (500, 450))
		if cf.read('activation_code') == '':
			label = myfont.render("Manage your device:", 1, WHITE)
			screen.blit(label, (50, 500))
			label = myfont.render("wzc.waaromzomoeilijk.nl", 1, GREEN)
			screen.blit(label, (500, 500))
		# show the whole thing
		pygame.display.flip()

	index_html = '''
<html>
<head>
	<title>WaaromZoCloud</title>
	<meta http-equiv="refresh" content="3" />
	<style type="text/css">
body {
	font-size: 5px; font-family: Verdana, Arial, "sans-serif"; color: yellow; background-color: black;
}
table{
	font-size: 33px;
}
</style>
<body><br><br><br><br><br>
<table width=100%>
<tr>
	<td align=left>Device ID: 
	<td>cccc
	<td>
</tr>
aaaa
<tr>
	<td align=list>Please sign up & add your new device:
	<td>https://wzc.waaromzomoeilijk.nl
</tr>
</table></body></html>
'''

#	index_html = index_html.replace('iiii',str(cf.read('id')))
	index_html = index_html.replace('cccc',ssm.computernr)
	if cf.read('activation_code') == '':
		index_html = index_html.replace('Temporary ','')
		index_html = index_html.replace('aaaa','')
		index_html = index_html.replace('content="3"','content="60"')
		check_again = 60
	else:
		index_html = index_html.replace('aaaa','<tr><td align=left>Activation code: <td>' + cf.read('activation_code') + '</tr>')
		check_again = 1
	f=open('/var/www/index.html','w+')
	f.write(index_html)
	f.close()
	tteller += 1
	print('ppp: ' + str(tteller))
	sleep(check_again)
