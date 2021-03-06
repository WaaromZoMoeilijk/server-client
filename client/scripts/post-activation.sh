#!/bin/bash
# shellcheck disable=SC2034,SC1090,SC2002,SC2046
# info@waaromzomoeilijk.nl
###############################################################################################################
# LOGGER                                                                                                      #
###############################################################################################################
INTERACTIVE="0" # 1 Foreground / 0 = Background - Log all script output to file (0) or just output everything in stout (1)
if [ $INTERACTIVE == 0 ]; then 
    LOGFILE="/var/log/post_activation.log" # Log file
    exec 3>&1 4>&2
    trap 'exec 2>&4 1>&3' 0 1 2 3 15 RETURN
    exec 1>>"$LOGFILE" 2>&1
fi

###############################################################################################################
# VARIABLES AND FUNCTIONS                                                                                     #
###############################################################################################################
source <(curl -sL https://raw.githubusercontent.com/WaaromZoMoeilijk/server-client/main/client/lib.sh)

# Tmp fix to get ssh port
#sudo python3 /home/dietpi/m.py ; wait

# Client config
CNFSRC='/home/dietpi/config.txt'
USERID=$(jq '.userid' < "$CNFSRC")
EMAIL=$(jq '.email' < "$CNFSRC")
NAMESERVER=$(jq '.nameserver' < "$CNFSRC")
REVERSESSHSERVER=$(jq '.reverse_ssh_server' < "$CNFSRC")
IPETH=$(jq '.ipAddressEth' < "$CNFSRC")
GATEWAY=$(jq '.gateway' < "$CNFSRC")
SUBNETMASK=$(jq '.subnetEth' < "$CNFSRC")
ACTIVATIONCODE=$(jq '.activation_code' < "$CNFSRC")
SSHPORT=$(jq '.ssh_port' < "$CNFSRC")
ID=$(jq '.id' < "$CNFSRC")

###############################################################################################################
# INIT                                                                                                        #
###############################################################################################################
DEBUG=1
debug_mode
root_check

###############################################################################################################
# CREATE NC USER                                                                                              #
###############################################################################################################
(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | /usr/bin/su -s /bin/sh www-data -c "/usr/bin/php /var/www/nextcloud/occ user:add --group admin $USERNAME"
#(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | /usr/bin/su -s /bin/sh www-data -c "/usr/bin/php /var/www/nextcloud/occ user:resetpassword $USERNAME"

###############################################################################################################
# ENABLE NC USER                                                                                              #
###############################################################################################################
#/usr/bin/su -s /bin/sh www-data -c "/usr/bin/php /var/www/nextcloud/occ user:enable $USERNAME"

###############################################################################################################
# ACTIVATE USER                                                                                               #
###############################################################################################################
curl -vv --user "$USERNAME":"$PASSWORD" "http://127.0.0.1/nextcloud/login?clear=1"
echo "Curl login"

###############################################################################################################
# CREATE PAM USER                                                                                             #
###############################################################################################################
/usr/bin/sudo useradd -m -p $(openssl passwd -crypt "$PASSWORD") "$USERNAME"
# Reset pass if user exists
#(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | passwd "$USERNAME"
echo "Pam"

###############################################################################################################
# CHANGE ROOT PASS                                                                                            #
###############################################################################################################
(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | passwd root
echo "Root pass change"

###############################################################################################################
# SMB USER                                                                                                    #
###############################################################################################################
(/usr/bin/echo "$PASSWORD"; /usr/bin/echo "$PASSWORD") | /usr/bin/sudo smbpasswd -as "$USERNAME" 
echo "SMB"

###############################################################################################################
# SMB USER WWW-DATA GROUP                                                                                     #
###############################################################################################################
usermod -aG www-data "$USERNAME"
echo "Samba add user to www-data group"

###############################################################################################################
# EXTERNAL FILES APP                                                                                          #
###############################################################################################################
/usr/bin/sudo -u www-data php /var/www/nextcloud/occ app:enable files_external
echo "NC External files app"

###############################################################################################################
# SMB CONFIG                                                                                                  #
###############################################################################################################
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

###############################################################################################################
# CREATE DIRS                                                                                                 #
###############################################################################################################
mkdir -p /var/log/samba 
#mkdir -p /mnt/dietpi_userdata/"$USERNAME"
echo "Created Dirs"

###############################################################################################################
# PERMISSIONS                                                                                                 #
###############################################################################################################
#chown "$USERNAME":"$USERNAME" /mnt/dietpi_userdata/"$USERNAME"
chmod -R 770 /mnt/dietpi_userdata/nextcloud_data/"$USERNAME"/files
echo "Set permission"

###############################################################################################################
# RESTART SMB                                                                                                 #
###############################################################################################################
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

###############################################################################################################
# CRON                                                                                                        #
###############################################################################################################
crontab -l | { cat; echo "* * * * * pgrep 'php' || sudo -u www-data php /var/www/nextcloud/occ files:scan $USERNAME"; } | crontab -
#crontab -l | { cat; echo "@reboot sudo -u www-data php /var/www/nextcloud/occ files_external:notify 1"; } | crontab -
echo "Crontab"

###############################################################################################################
# RM WEBPAGE SETUP DETAILS                                                                                    #
###############################################################################################################
# Remove webpage setup details
#rm /home/dietpi/a.py
rm /var/www/index.html

###############################################################################################################
# REVERT SUBFOLDER TO WEBROOT                                                                                 #
###############################################################################################################
# Revert subfolder to webroot and more
sed -i "s|.*overwrite.cli.url.*|  'overwrite.cli.url' => 'https://$USERNAME.$DOMAIN/',|g" /var/www/nextcloud/config/config.php
sed -i "s|.*htaccess.RewriteBase.*|  'htaccess.RewriteBase' => '/',|g" /var/www/nextcloud/config/config.php
sed -i "s|.*ErrorDocument 403.*|ErrorDocument 403 /|g" /var/www/nextcloud/.htaccess
sed -i "s|.*ErrorDocument 404.*|ErrorDocument 404 /|g" /var/www/nextcloud/.htaccess
sed -i "s|.*RewriteBase.*|  RewriteBase /|g" /var/www/nextcloud/.htaccess
sed -i "s|DocumentRoot /var/www|DocumentRoot /var/www/nextcloud|g" /etc/apache2/sites-enabled/000-default.conf  

###############################################################################################################
# FORCE CONSOLE SIZE                                                                                          #
###############################################################################################################
# Force a console size. By default it will be display's size minus overscan.
# Needs an auto check for available resolution
#sed -i "s|.*framebuffer_width.*|framebuffer_width=1920|g" /boot/config.txt
#sed -i "s|.*framebuffer_height.*|framebuffer_height=1080|g" /boot/config.txt

###############################################################################################################
# STATIC IP                                                                                                   #
###############################################################################################################
cat > '/etc/network/interfaces' <<EOF
# Location: /etc/network/interfaces
# Please modify network settings via: dietpi-config
# Or create your own drop-ins in: /etc/network/interfaces.d/

# Drop-in configs
source interfaces.d/*

# Ethernet
allow-hotplug eth0
iface eth0 inet static
address $ADDRESS
netmask $NETMASK
gateway $GATEWAY
dns-nameservers 1.1.1.1 1.0.0.1

# WiFi
#allow-hotplug wlan0
iface wlan0 inet static
address $ADDRESS
netmask $NETMASK
gateway $GATEWAY
dns-nameservers 1.1.1.1 1.0.0.1
wireless-power off
wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf
EOF

#sed -i "s|iface eth0 inet dhcp|iface $IFACE inet static|g" /etc/network/interfaces
#sed -i "s|gateway 192.168.0.1|gateway $GATEWAY|g" /etc/network/interfaces
#sed -i "s|address 192.168.0.100|ADDRESS $ADDRESS|g" /etc/network/interfaces
#sed -i "s|netmask 255.255.255.0|netmask $NETMASK|g" /etc/network/interfaces
#sed -i "s|#dns-nameservers 9.9.9.9 149.112.112.112|dns-nameservers 1.1.1.1 1.0.0.1|g" /etc/network/interfaces

###############################################################################################################
# CONFIG VALUES NC                                                                                            #
###############################################################################################################

/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ config:system:set trusted_domains 0 --value localhost"
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ config:system:set trusted_domains 1 --value $ADDRESS"
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ config:system:set trusted_domains 2 --value $USERNAME.$DOMAIN"
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ config:system:set trusted_domains 3 --value 192.168.22.2"
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ config:system:set trusted_proxy 0 --value wzc.$DOMAIN"
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ config:system:set trusted_proxy 1 --value $USERNAME.$DOMAIN"
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ config:system:set trusted_proxy 2 --value 192.168.22.2"
/usr/bin/su -s /bin/sh www-data -c "php /var/www/nextcloud/occ config:system:set trusted_proxy 3 --value  $ADDRESS"

###############################################################################################################
# IFRAME CONFIG                                                                                               #
###############################################################################################################
# Allow iFrame only from wzc.waaromzomoeilijk.nl for webframe of user cloud
sed -i 's|</Directory>|        Header set X-Frame-Options: "ALLOW_FROM https://wzc.waaromzomoeilijk.nl"|g' /etc/apache2/sites-available/dietpi-nextcloud.conf
echo '        Header set Content-Security-Policy: "frame-ancestors https://wzc.waaromzomoeilijk.nl"' >> /etc/apache2/sites-available/dietpi-nextcloud.conf
echo "</Directory>" >> /etc/apache2/sites-available/dietpi-nextcloud.conf

###############################################################################################################
# CRON                                                                                                        #
###############################################################################################################
# Setup tunnel checker every minute
crontab -l | { cat; echo "* * * * * /bin/bash $GITDIR/client/scripts/tunnel_check.sh"; } | crontab -

###############################################################################################################
# WRAP UP                                                                                                     #
###############################################################################################################
"$(date)" >> /home/dietpi/.install_success

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
