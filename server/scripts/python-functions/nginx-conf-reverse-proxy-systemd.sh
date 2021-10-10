#!/bin/bash
# Setup Systemd service that starts the inotify service that in turn checks wether new devices have registered and adds them as a subdomain in nginx

mkdir -p /var/scripts
wget -P /var/scripts https://raw.githubusercontent.com/WaaromZoMoeilijk/server-client/main/server/scripts/python-functions/nginx-conf-reverse-proxy.sh
chmod 750 /var/scripts/nginx-conf-reverse-proxy.sh

if [ -f "/etc/systemd/system/nginx-conf-reverse-proxy.service" ]; then
      echo "/etc/systemd/system/nginx-conf-reverse-proxy.service exists"
else  
cat > /etc/systemd/system/nginx-conf-reverse-proxy.service <<EOF
[Unit]
Description=Proxy checker nginx
Type=simple

[Service]
ExecStart=/var/scripts/nginx-conf-reverse-proxy.sh --full --to-external
Restart=on-failure
PIDFile=/tmp/nginx-conf-reverse-proxy.pid
#User=srvuser
#WorkingDirectory=/var/yourservice
#RuntimeDirectory=yourservice
#RuntimeDirectoryMode=0755

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable nginx-conf-reverse-proxy.service
systemctl start nginx-conf-reverse-proxy.service
fi

exit 0
