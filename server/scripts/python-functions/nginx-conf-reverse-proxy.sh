#!/bin/bash

inotifywait -m /var/www/pi/rpi_info -e create -e moved_to |
while read dir action file; do
	echo "The file '$file' appeared in directory '$dir' via '$action'"

	DATE=$(date)
	PUBKEY=$(cat "$dir/$file" | jq -r .pubkey)
        USERNAME=$(cat "$dir/$file" | jq -r .userid)
	NGINXCONF=$(echo "$file" | sed 's|.json|.conf|g')
        SSHPORT=$(cat "$dir/$file" | jq -r .ssh_port)

	# Get Nginx config
	wget -O /etc/nginx/sites-enabled/"$NGINXCONF" https://raw.githubusercontent.com/WaaromZoMoeilijk/server-client/main/client/scripts/proxy.conf

	# Change subdomain and proxy port
	sed -i "s|USERNAME|$USERNAME|g" /etc/nginx/sites-enabled/"$NGINXCONF"
	sed -i "s|SSHPORT|$SSHPORT|g" /etc/nginx/sites-enabled/"$NGINXCONF"
        sed -i "s|wzc-|$USERNAME-|g" /etc/nginx/sites-enabled/"$NGINXCONF"

	# Check config
	nginx -t || echo "Failed to set config please manually check" ; exit 1

	# Set pubkey
	echo "$file added on $DATE" >> /home/remote/.ssh/authorized_keys
	echo "$PUBKEY" >> /home/remote/.ssh/authorized_keys
	echo

	# Reload new config
	service nginx reload
done
