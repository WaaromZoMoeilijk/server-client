#!/bin/bash

# $PASSWORD en $USERNAME should be reused during registration in django to create a nextcloud and system user that has the same credentials.
# Note these commands need to be executed on the client with the PASSWORD AND USERNAME variable from the server
/usr/bin/sudo -u www-data export OC_PASS="$PASSWORD" 
/usr/bin/sudo -u www-data php /var/www/nextcloud/occ user:add --password-from-env --GROUP="admin" "$USERNAME" 
/usr/bin/sudo useradd -m -p $(openssl passwd -crypt "$PASSWORD") "$USERNAME" 
/usr/bin/sudo -u www-data export OC_PASS=""
