#!/bin/bash
# info@waaromzomoeilijk.nl

###################################
# Variables & functions
source <(curl -sL https://raw.githubusercontent.com/ezraholm50/server-client/main/client/lib.sh)

# Client config
CNFSRC='/home/dietpi/config.txt'
USERID=$(cat "$CNFSRC" | jq '.userid')
EMAIL=$(cat "$CNFSRC" | jq '.email')
NAMESERVER=$(cat "$CNFSRC" | jq '.nameserver')
REVERSESSHSERVER=$(cat "$CNFSRC" | jq '.reverse_ssh_server')
IPETH=$(cat "$CNFSRC" | jq '.ipAddressEth')
GATEWAY=$(cat "$CNFSRC" | jq '.gateway')
SUBNETMASK=$(cat "$CNFSRC"| jq '.subnetEth')
ACTIVATIONCODE=$(cat "$CNFSRC" | jq '.activation_code')
SSHPORT=$(cat "$CNFSRC" | jq '.ssh_port')
ID=$(cat "$CNFSRC" | jq '.id')

# Check for errors + debug code and abort if something isn't right
# 1 = ON
# 0 = OFF
DEBUG=1
debug_mode

# Check if script runs as root
root_check

# Create NC user
(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | /usr/bin/su -s /bin/sh www-data -c "/usr/bin/php /var/www/nextcloud/occ user:add --group admin $USERNAME"
#(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | /usr/bin/su -s /bin/sh www-data -c "/usr/bin/php /var/www/nextcloud/occ user:resetpassword $USERNAME"

# Enable NC user
#/usr/bin/su -s /bin/sh www-data -c "/usr/bin/php /var/www/nextcloud/occ user:enable $USERNAME"

# Activate user
curl -vv --user "$USERNAME":"$PASSWORD" "http://127.0.0.1/nextcloud/login?clear=1"
echo "Curl login"

# Create PAM user
/usr/bin/sudo useradd -m -p $(openssl passwd -crypt "$PASSWORD") "$USERNAME"
# Reset pass if user exists
#(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | passwd "$USERNAME"
echo "Pam"

# Create SMB user
(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | /usr/bin/sudo smbpasswd -as "$USERNAME" 
echo "SMB"

# Samba
usermod -aG www-data "$USERNAME"
echo "Samba add user to www-data group"

# Enable external files app
/usr/bin/sudo -u www-data php /var/www/nextcloud/occ app:enable files_external
echo "NC External files app"

# Add samba config
if [ -f "/etc/samba/smb.conf" ]; then
cat >> /etc/samba/smb.conf <<EOF
[$USERNAME]
valid users = @www-data
Path = /mnt/dietpi_userdata/nextcloud_data/$USERNAME/files
Browseable = yes
Writeable = Yes
Guest ok = no
Public = no
force group = www-data
create mask = 0770
directory mask = 0771
force create mode = 0660
force directory mode = 0770
EOF
else  
echo "smb.conf doesn't exists, is it installed?"
apt install -y samba samba-common-bin smbclient
	
cat >> /etc/samba/smb.conf <<EOF
[$USERNAME]
valid users = @www-data
Path = /mnt/dietpi_userdata/nextcloud_data/$USERNAME/files
Browseable = yes
Writeable = Yes
Guest ok = no
Public = no
force group = www-data
create mask = 0770
directory mask = 0771
force create mode = 0660
force directory mode = 0770
EOF
fi
echo "Samba config set"

# Create dirs
mkdir -p /var/log/samba 
#mkdir -p /mnt/dietpi_userdata/"$USERNAME"
echo "Created Dirs"

# Permissions
#chown "$USERNAME":"$USERNAME" /mnt/dietpi_userdata/"$USERNAME"
chmod -R 770 /mnt/dietpi_userdata/nextcloud_data/"$USERNAME"/files
echo "Set permission"

# Restart smbd
service smbd restart && sleep 10
echo "SMBD restarted"

# Create external user share
#/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ files_external:create --user $USERNAME / smb password::password" | awk '{print $5}' > /home/dietpi/.smbid."$USERNAME"
#echo "Created external user share"
# Set config
#SMBID=$(cat /home/dietpi/.smbid."$USERNAME")
#echo "id"
#/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ files_external:config $SMBID host 127.0.0.1"
#echo "host"
#/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ files_external:config $SMBID share $USERNAME"
#echo "share"
#/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ files_external:config $SMBID username $USERNAME"
#echo "user"
#/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ files_external:config $SMBID password $PASSWORD"
#echo "pass"
#/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ files_external:config $SMBID enable_sharing true"
#echo "sharing"

# cronjob to check for files smb vs nc
crontab -l | { cat; echo "* * * * * pgrep "php" || sudo -u www-data php /var/www/nextcloud/occ files:scan $USERNAME"; } | crontab -
#crontab -l | { cat; echo "@reboot sudo -u www-data php /var/www/nextcloud/occ files_external:notify 1"; } | crontab -
echo "Crontab"

# Remove webpage setup details
rm /home/dietpi/a.py
rm /var/www/index.html

# Revert subfolder to webroot
sed -i "s|.*overwrite.cli.url.*|  'overwrite.cli.url' => 'https://$USERNAME.$DOMAIN/',|g" /var/www/nextcloud/config/config.php
sed -i "s|.*htaccess.RewriteBase.*|  'htaccess.RewriteBase' => '/',|g" /var/www/nextcloud/config/config.php
sed -i "s|.*ErrorDocument 403.*|ErrorDocument 403 /|g" /var/www/nextcloud/.htaccess
sed -i "s|.*ErrorDocument 404.*|ErrorDocument 404 /|g" /var/www/nextcloud/.htaccess
sed -i "s|.*RewriteBase.*|  RewriteBase /|g" /var/www/nextcloud/.htaccess

# Set config values for nextcloud
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ config:system:set trusted_domains 1 --value localhost"
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ config:system:set trusted_domains 2 --value $USERNAME.$DOMAIN"
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ config:system:set trusted_proxy 1 --value $USERNAME.$DOMAIN"

# Setup tunnel checker every minute
crontab -l | { cat; echo "* * * * * /bin/bash $GITDIR/client/scripts/tunnel_check.sh"; } | crontab -

# install complete
touch /home/dietpi/.install_success

# Unset password var
unset PASSWORD
echo "Unset pass"

# Delete admin
# Leftover fix in final image
#/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ user:delete admin" && echo "Default admin removed"
#rm -rf /mnt/dietpi_userdata/nextcloud_data/ezrawzm
#/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ user:delete ezrawzm"

# Reboot
reboot
