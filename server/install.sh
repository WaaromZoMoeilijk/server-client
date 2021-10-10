#!/bin/bash
# info@waaromzomoeilijk.nl

###################################
# Variables & functions
source <(curl -sL https://raw.githubusercontent.com/ezraholm50/server-client/main/client/lib.sh)

apt install -y \
       python3-virtualenv \
       apache2 \
       libapache2-mod-wsgi-py3 \
       inotify-tools

crontab -l | { cat; echo "* * * * * /usr/bin/sudo /usr/bin/python3 /var/www/pi/pidjango/rpi_info.py"; } | crontab -

CAT
<VirtualHost *:2021>
        ServerName wzc.waaromzomoeilijk.nl
        ServerAlias *
        DocumentRoot /var/www/html
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        SSLEngine on
        SSLCertificateFile      /etc/letsencrypt/live/henk.waaromzomoeilijk.nl/fullchain.pem
        SSLCertificateKeyFile   /etc/letsencrypt/live/henk.waaromzomoeilijk.nl/privkey.pem
#       SSLCertificateFile      /etc/ssl/certs/nginx-selfsigned.crt
#       SSLCertificateKeyFile  /etc/ssl/private/nginx-selfsigned.key

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined
#	Redirect permanent "/" "https://henk.waaromzomoeilijk.nl:2021/"

        Alias /static /var/www/pi/pidjango/static
        <Directory /var/www/pi/pidjango/static>
                Require all granted
        </Directory>

        <Directory /var/www/pi/pidjango/pidjango>
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>

        WSGIDaemonProcess django-http python-path=/var/www/pi/pidjango python-home=/var/www/pi/env
        WSGIProcessGroup django-http
        WSGIScriptAlias / /var/www/pi/pidjango/pidjango/wsgi.py

</VirtualHost>



find /var/www/pi -type f -exec chmod 0640 {} +
find /var/www/pi -type d -exec chmod 0750 {} +
chown -R www-data:www-data /var/www/pi

python3 server.py

exit 0
