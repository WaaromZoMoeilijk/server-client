#!/bin/bash
# info@waaromzomoeilijk.nl

###################################
# Variables & functions
source <(curl -sL https://raw.githubusercontent.com/ezraholm50/server-client/main/client/lib.sh)

apt install python3-virtualenv


nginx
server {
       listen 2020;

       server_name _;

         location /static/ {
                root /home/dietpi/pidjango;
               # add_header Cache-Control "public, max-age=86400" always;
        }
       location / {
                include proxy_params;
                proxy_pass http://unix:/home/dietpi/pidjango/gunicorn.sock;
        }
}


python3 server.py

exit 0
