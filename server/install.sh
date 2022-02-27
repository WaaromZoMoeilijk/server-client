#!/bin/bash
# scripting@waaromzomoeilijk.nl
# shellcheck disable=SC1091,SC2164,SC2154

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
git clone server /opt 
mkdir -p "$DIRECTORY"
mv /opt/server/* "$DIRECTORY"
find "$DIRECTORY"  -type f -exec chmod 0640 {} +
find "$DIRECTORY"  -type d -exec chmod 0750 {} +
chown -R www-data:www-data "$DIRECTORY"

chmod +x /opt/server-client/server/scripts/python-functions/*.sh

###############################################################################################################
# DJANGO                                                                                                      #
###############################################################################################################
cd "$DIRECTORY" 
python3 -m venv env
source env/bin/activate
pip3 install gunicorn django
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic

###############################################################################################################
# SETUP SERVER AS A SERVICE                                                                                   #
###############################################################################################################
cat > /etc/systemd/system/wzc.service <<EOF
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
# SETUP INOTIFY AS A SERVICE                                                                                  #
###############################################################################################################
cat > /etc/systemd/system/wzc_inotify.service <<EOF
[Unit]
Description=Inotify folder checker
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/pi/rpi_info
ExecStart=/bin/bash /opt/server-client/server/scripts/python-functions/nginx-conf-reverse-proxy.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable wzc_inotify.service
systemctl start wzc_inotify.service

###############################################################################################################
# DHPARAMS                                                                                                    #
###############################################################################################################
openssl dhparam -out /etc/ssl/certs/dhparam.pem 4096

###############################################################################################################
# NGINX CONFIG                                                                                                #
###############################################################################################################

cat > /etc/nginx/sites-available/wzc.conf <<EOF
server {
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
}

server {

       listen 443 ssl http2;

        server_name wzc.waaromzomoeilijk.nl;

        ssl_certificate /etc/letsencrypt/live/wzc.waaromzomoeilijk.nl/cert.pem;
        ssl_certificate_key /etc/letsencrypt/live/wzc.waaromzomoeilijk.nl/privkey.pem;

        # intermediate configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        ssl_dhparam /etc/ssl/certs/dhparam.pem;
        ssl_ecdh_curve secp384r1;
        ssl_session_timeout  10m;
        ssl_session_cache shared:SSL:10m;
        ssl_session_tickets off;

        # OCSP stapling
        ssl_stapling on;
        ssl_stapling_verify on;

        resolver 192.168.24.2 valid=300s;
        resolver_timeout 5s;

        # Disable strict transport security for now. You can uncomment the following
        # line if you understand the implications.
        #add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";


        location /static/ {
                root /var/www/pi/pidjango;
                # add_header Cache-Control "public, max-age=86400" always;
        }
       
        location / {
                include proxy.conf;
                proxy_pass http://unix:/var/www/pi/pidjango/gunicorn.sock;
        }
}

server {

       listen 2021 ssl http2;

        server_name wzc.waaromzomoeilijk.nl;

        ssl_certificate /etc/letsencrypt/live/wzc.waaromzomoeilijk.nl/cert.pem;
        ssl_certificate_key /etc/letsencrypt/live/wzc.waaromzomoeilijk.nl/privkey.pem;

        # intermediate configuration
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
        ssl_prefer_server_ciphers off;
        ssl_dhparam /etc/ssl/certs/dhparam.pem;
        ssl_ecdh_curve secp384r1;
        ssl_session_timeout  10m;
        ssl_session_cache shared:SSL:10m;
        ssl_session_tickets off;

        # OCSP stapling
        ssl_stapling on;
        ssl_stapling_verify on;

        resolver 192.168.24.2 valid=300s;
        resolver_timeout 5s;

        # Disable strict transport security for now. You can uncomment the following
        # line if you understand the implications.
        #add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";


        location /static/ {
                root /var/www/pi/pidjango;
                # add_header Cache-Control "public, max-age=86400" always;
        }
       
        location / {
                include proxy.conf;
                proxy_pass http://unix:/var/www/pi/pidjango/gunicorn.sock;
        }
}
EOF

systemctl daemon-reload
systemctl enable wzc.service
systemctl restart gunicorn
systemctl start wzc.service
systemctl restart nginx.service

exit 0