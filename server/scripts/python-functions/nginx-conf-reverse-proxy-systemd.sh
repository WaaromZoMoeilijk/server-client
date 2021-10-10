#!/bin/bash
# Setup Systemd service that starts the inotify service that in turn checks wether new devices have registered and adds them as a subdomain in nginx

mkdir -p /var/scripts
wget -P /var/scripts https://raw.githubusercontent.com/WaaromZoMoeilijk/server-client/main/server/scripts/python-functions/nginx-conf-reverse-proxy.sh
chmod +x /var/scripts/nginx-conf-reverse-proxy.sh

if [ -f "/etc/systemd/system/nginx-conf-reverse-proxy.service" ]; then
      echo "/etc/systemd/system/nginx-conf-reverse-proxy.service exists"
else  
cat > /etc/systemd/system/nginx-conf-reverse-proxy.service <<EOF
[Unit]
Description=Run script at startup after all systemd services are loaded
After=default.target

[Service]
Type=simple
RemainAfterExit=yes
StandardOutput=tty
ExecStart=/var/scripts/nginx-conf-reverse-proxy.sh
TimeoutStartSec=0

[Install]
WantedBy=default.target
EOF

systemctl daemon-reload
systemctl enable nginx-conf-reverse-proxy.service
fi

exit 0
