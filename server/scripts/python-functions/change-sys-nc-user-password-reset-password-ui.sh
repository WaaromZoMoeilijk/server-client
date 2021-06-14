#!/bin/bash

# When the user changes his password in the webui also reuse that password as a variable to change the linux and nextclouds users password.
# variable $NEWPASSWORD
/usr/bin/sudo -u www-data export OC_PASS="$NEWPASSWORD" 
/usr/bin/sudo -u www-data php /var/www/nextcloud/occ user:resetpassword --password-from-env "$USERNAME" 
/usr/bin/sudo echo "$USERNAME:$NEWPASSWORD" | chpasswd 
(echo "$NEWPASSWORD"; echo "$NEWPASSWORD") | /usr/bin/sudo smbpasswd -as "$USERNAME" 
/usr/bin/sudo -u www-data export OC_PASS=""
