#!/bin/bash
# info@waaromzomoeilijk.nl

###################################
# Variables & functions
set -e
source <(curl -sL https://raw.githubusercontent.com/ezraholm50/server-client/main/client/lib.sh)

# Check for errors + debug code and abort if something isn't right
# 1 = ON
# 0 = OFF
DEBUG=1
debug_mode

# Check if script runs as root
root_check

# Check if device is activated
#if [ "$ACTIVATIONCODE" == '""' ]; then 
#        echo "registered"
#else
#        echo "device not registered yet."
#	exit 1
#fi

# Create NC user
(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | /usr/bin/su -s /bin/sh www-data -c "/usr/bin/php /var/www/nextcloud/occ user:add --group admin $USERNAME"
#(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | /usr/bin/su -s /bin/sh www-data -c "/usr/bin/php /var/www/nextcloud/occ user:resetpassword $USERNAME"

# Create PAM user
/usr/bin/sudo useradd -m -p $(openssl passwd -crypt "$PASSWORD") "$USERNAME"  

# Create SMB user
(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | /usr/bin/sudo smbpasswd -as "$USERNAME" 

# Enable external files app
/usr/bin/sudo -u www-data php /var/www/nextcloud/occ app:enable files_external

# Add samba config
if [ -f "/etc/samba/smb.conf" ]; then
cat >> /etc/samba/smb.conf <<EOF
["$USERNAME"]
valid users = "$USERNAME"
Path = /mnt/dietpi_userdata/SAMBA/"$USERNAME"
Browseable = yes
Writeable = Yes
create mask = 0770
directory mask = 0770
Public = no
EOF
else  
echo "smb.conf doesn't exists, is it installed?"
apt install -y samba samba-common-bin smbclient
	
cat >> /etc/samba/smb.conf <<EOF
["$USERNAME"]
valid users = "$USERNAME"
Path = /mnt/dietpi_userdata/SAMBA/"$USERNAME"
Browseable = yes
Writeable = Yes
create mask = 0770
directory mask = 0770
Public = no
EOF
fi

# Create dirs
mkdir -p /mnt/dietpi_userdata/SAMBA 
mkdir -p /mnt/dietpi_userdata/SAMBA/"$USERNAME"

# Permissions
chown dietpi:dietpi /mnt/dietpi_userdata/SAMBA
chown "$USERNAME":"$USERNAME" /mnt/dietpi_userdata/SAMBA/"$USERNAME"

# Add smb user ; done in python upon registering
#(echo "$PASSWORD"; echo "$PASSWORD") | smbpasswd -a "$USERNAME"

# Restart smbd
service smbd restart

# Config smb
cat > /tmp/smb.json <<EOF
[
    {
        "mount_id": 1,
        "mount_point": "\/",
        "storage": "\\\OCA\\\Files_External\\\Lib\\\Storage\\\SMB",
        "authentication_type": "password::password",
        "configuration": {
            "host": "127.0.0.1",
            "share": "$USERNAME",
            "root": "",
            "domain": "",
            "show_hidden": false,
            "check_acl": false,
            "timeout": "",
            "user": "$USERNAME",
            "password": ""
        },
        "options": {
            "encrypt": true,
            "previews": true,
            "enable_sharing": true,
            "filesystem_check_changes": 1,
            "encoding_compatibility": false,
            "readonly": false
        },
        "applicable_users": [
            "$USERNAME"
        ],
        "applicable_groups": [],
        "type": "$USERNAME"
    }
]
EOF

# Permissions
chown www-data /tmp/smb.json

# Import SMB config, password will get set upon activation via python
#sudo -u www-data php /var/www/nextcloud/occ files_external:option 1 password "$PASSWORD"
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ files_external:import /tmp/smb.json" && rm -rf /tmp/smb.json

# Setup share NC
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ files_external:option 1 password $PASSWORD"

# cronjob to check for files
crontab -l | { cat; echo "2 0 0 0 sudo -u www-data php /var/www/nextcloud/occ files:scan --all"; } | crontab -
crontab -l | { cat; echo "@reboot sudo -u www-data php /var/www/nextcloud/occ files_external:notify 1"; } | crontab -

# Clear pass var
#sed -i 's|PASSWORD=*|PASSWORD=""|g' "$GITDIR"/client/scripts/post-activation.sh

# install complete
touch /home/dietpi/.smb_success

# Unset password var
unset PASSWORD

exit 0
