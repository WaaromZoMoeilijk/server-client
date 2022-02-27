#!/bin/bash
# shellcheck disable=SC2001

inotifywait -m /var/www/pi/rpi_info -e create -e moved_to |
while read -r dir action file; do
        echo "The file '$file' appeared in directory '$dir' via '$action'"

        DATE=$(date)
        PUBKEY=$(jq -r .pubkey < "$dir/$file")
        USERNAME=$(jq -r .userid < "$dir/$file")
        NGINXCONF=$(echo "$file" | sed 's|.json|.conf|g')
        SSHPORT=$(jq -r .ssh_port < "$dir/$file")

        # Get Nginx config
        wget -O /etc/nginx/sites-enabled/"$NGINXCONF" https://raw.githubusercontent.com/WaaromZoMoeilijk/server-client/main/client/scripts/proxy.conf

        # Change subdomain and proxy port
        sed -i "s|USERNAME|$USERNAME|g" /etc/nginx/sites-enabled/"$NGINXCONF"
        sed -i "s|SSHPORT|$SSHPORT|g" /etc/nginx/sites-enabled/"$NGINXCONF"
        sed -i "s|wzc-|$USERNAME-|g" /etc/nginx/sites-enabled/"$NGINXCONF"

        # Check config
        nginx -t || echo "Failed to set config please manually check" 

        # Set pubkey
        mkdir -p /home/remote/.ssh
        {
        echo "$file added on $DATE"
        echo "$PUBKEY"
        echo
        } >> /home/remote/.ssh/authorized_keys

        # Reload new config
        service nginx reload
done