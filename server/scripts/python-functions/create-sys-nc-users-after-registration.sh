#!/bin/bash

# $PASSWORD en $USERNAME should be reused during registration in django to create a nextcloud and system user that has the same credentials.
# Note these commands need to be executed on the client with the PASSWORD AND USERNAME variable from the server
export OC_PASS="$PASSWORD" 
#/usr/bin/sudo -u www-data php /var/www/nextcloud/occ user:add --password-from-env --group "admin" "$USERNAME" 
su -s /bin/sh www-data -c 'php /var/www/nextcloud/occ user:add --password-from-env --group "admin" "$USERNAME" EMAIL'
/usr/bin/sudo useradd -m -p $(openssl passwd -crypt "$PASSWORD") "$USERNAME" 
(echo "$PASSWORD"; echo "$PASSWORD") | /usr/bin/sudo smbpasswd -as "$USERNAME"
sudo -u www-data php /var/www/nextcloud/occ files_external:option 1 password "$PASSWORD"
export OC_PASS=""
reboot
