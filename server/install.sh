#!/bin/bash
# scripting@waaromzomoeilijk.nl

###############################################################################################################
# VARIABLES                                                                                                    #
###############################################################################################################
DIRECTORY="/var/www/pi"

###############################################################################################################
# REQUIRED                                                                                                    #
###############################################################################################################
apt install -y \
       python3 \
       python3-pip \
       python3-virtualenv \
       nginx \
       fail2ban \
       inotify-tools

###############################################################################################################
# AUTO REVERSE PROXY ADDING MONITOR                                                                           #
###############################################################################################################
crontab -l | { cat; echo "* * * * * /usr/bin/sudo /usr/bin/python3 /var/www/pi/pidjango/rpi_info.py"; } | crontab -

###############################################################################################################
# GIT CLONE SERVER                                                                                            #
###############################################################################################################
git clone server "$DIRECTORY"
find /var/www/pi -type f -exec chmod 0640 {} +
find /var/www/pi -type d -exec chmod 0750 {} +
chown -R www-data:www-data /var/www/pi

###############################################################################################################
# DJANGO                                                                                                      #
###############################################################################################################
cd "$DIRECTORY" 
python3 -m venv env
#source env/bin/activate
pip3 install gunicorn django
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

###############################################################################################################
# SETUP SERVER AS A SERVICE                                                                                   #
###############################################################################################################
cat > /etc/systmd/system/wzc.service <<EOF
[Unit]
Description=WZC
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/pi/pidjango
ExecStart=/var/www/pi/pidjango/env/bin/gunicorn --reload --access-logfile - --workers 5 --bind unix:/var/www/pi/pidjango/gunicorn.sock pidjango.wsgi:application

[Install]
WantedBy=multi-user.target

EOF

###############################################################################################################
# DHPARAMS                                                                                                    #
###############################################################################################################
openssl dhparam -out /etc/ssl/certs/dhparam.pem 4096

###############################################################################################################
# NGINX CONFIG                                                                                                #
###############################################################################################################

cat > /etc/nginx/sites-available/wzc.conf <<EOF

EOF

systemctl deamon-reload
systemctl enable wzc.service
systemctl restart gunicorn
systemctl start wzc.service
systemctl restart nginx.service

exit 0