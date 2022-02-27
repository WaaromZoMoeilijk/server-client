#!/bin/bash
# shellcheck disable=SC2034,SC1090,SC2015
# info@waaromzomoeilijk.nl
# login root/raspberry, dietpi/raspberry
###############################################################################################################
# DEFAULT LOG EXTENSION                                                                                       #
###############################################################################################################
# && success "$(date) -  - " || fatal "$(date) -  - "

###############################################################################################################
# LOGGER                                                                                                      #
###############################################################################################################
INTERACTIVE="0" # 1 Foreground / 0 = Background - Log all script output to file (0) or just output everything in stout (1)
if [ $INTERACTIVE == 0 ]; then 
    LOGFILE="/var/log/WZC_INSTALL.log" # Log file
    exec 3>&1 4>&2
    trap 'exec 2>&4 1>&3' 0 1 2 3 15 RETURN
    exec 1>>"$LOGFILE" 2>&1
fi
###############################################################################################################
# VARS & FUNCTIONS                                                                                            #
###############################################################################################################
source <(curl -sL https://raw.githubusercontent.com/WaaromZoMoeilijk/server-client/main/client/lib.sh)

###############################################################################################################
# DEBUG                                                                                                       #
###############################################################################################################
# Check for errors + debug code and abort if something isn't right | 1 = ON / 0 = OFF
header "$(date) - DEBUG"
DEBUG=1
debug_mode && success "$(date) - DEBUG - Set!" || fatal "$(date) - DEBUG - Failed to set!"

###############################################################################################################
# ROOT CHECK                                                                                                  #
###############################################################################################################
header "$(date) - ROOT CHECK"
root_check && success "$(date) - PRE - Root check ok!" || fatal "$(date) - PRE - Failed root check!"

###############################################################################################################
# IPV4 OVER IPV6                                                                                              #
###############################################################################################################
header "$(date) - APT"
echo 'Acquire::ForceIPv4 "true";' > /etc/apt/apt.conf.d/99force-ipv4 && success "$(date) - APT - Force apt to use IPV4" || fatal "$(date) - APT - Failed to set apt to use IPV4"

###############################################################################################################
# UPDATE                                                                                                      #
###############################################################################################################
header "$(date) - UPDATE" 
export "DEBIAN_FRONTEND=noninteractive" 
export "DEBIAN_PRIORITY=critical"
apt_autoclean && success "$(date) - UPDATE - Autoclean!" || fatal "$(date) - UPDATE - Failed to autoclean!"
apt_autoremove && success "$(date) - UPDATE - Autoremoved!" || fatal "$(date) - UPDATE - Failed to autoremove!"
apt_update && success "$(date) - UPDATE - Updated!" || fatal "$(date) - UPDATE - Failed to update!"
apt_upgrade && success "$(date) - UPDATE - Upgraded!" || fatal "$(date) - UPDATE - Failed to upgrade!"

###############################################################################################################
# DEPENDENCIES                                                                                                #
###############################################################################################################
header "$(date) - DEPENDENCIES"
apt install -y \
	jq \
	git \
	nano \
	curl \
	autossh \
	unattended-upgrades \
	sshpass \
	net-tools \
	samba \
	smbclient \
	samba-common-bin \
	python3 \
	python3-pip \
	python3-pygame \
	python3-requests \
	python3-setuptools \
	python3-requests \
	openssh-server \
	avahi-daemon \
	libnss-mdns \
	php-pear \
	moreutils \
	miniupnpc && success "$(date) - DEPENDENCIES - Installed!" || fatal "$(date) - DEPENDENCIES - Failed to install!"

# Fix nextcloud issue on dietpi
#sed -i 's/128$//' /etc/php/*/cli/conf.d/98-dietpi-nextcloud.ini
#sed -i 's/256$//' /etc/php/*/cli/conf.d/98-dietpi-nextcloud.ini

###############################################################################################################
# TIMEZONE                                                                                                    #
###############################################################################################################
# Set timezone based upon WAN ip 
header "$(date) - TIMEZONE"
curl -s --location --request GET 'https://api.ipgeolocation.io/timezone?apiKey=bbebedbbace2445386c258c0a472df1c' | jq '.timezone' | xargs timedatectl set-timezone && success "$(date) - TIMEZONE - Set based on WAN IP!" || fatal "$(date) - TIMEZONE - Failed to set based on WAN IP!"

###############################################################################################################
# UNATTENDED-UPGRADES                                                                                         #
###############################################################################################################
header "$(date) - UNATTENDED-UPGRADES"
DEBIAN_FRONTEND=noninteractive dpkg-reconfigure unattended-upgrades && success "$(date) - UNATTENDED-UPGRADES - Updated!" || fatal "$(date) - UNATTENDED-UPGRADES - Failed to update!"

###############################################################################################################
# RC.LOCAL                                                                                                    #
###############################################################################################################
header "$(date) - RCLOCAL"
echo "Adding RC.local"

if [ -f "/etc/rc.local" ]; then
      warning "RC.local exists"
else  

cat > /etc/systemd/system/rc-local.service <<EOF
[Unit]
Description=/etc/rc.local
ConditionPathExists=/etc/rc.local
[Service]
Type=forking
ExecStart=/etc/rc.local start
TimeoutSec=0
StandardOutput=tty
RemainAfterExit=yes
SysVStartPriority=99
[Install]
WantedBy=multi-user.target
EOF

# Add rc.local file
cat > /etc/rc.local <<EOF
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.
# Run info screen on HDMI and Web
# Start info screen on HDMI and Web

exit 0
EOF

# Set execute permission
chmod +x /etc/rc.local

# Enable service
systemctl enable rc-local

# Start service
systemctl start rc-local

#sed -i 's|exit 0|/usr/bin/python3 /home/dietpi/a.py &|g' /etc/rc.local
#echo >> /etc/rc.local
#echo "exit 0" >> /etc/rc.local

fi

###############################################################################################################
# SSH KEYS                                                                                                    #
###############################################################################################################
header "$(date) - SSH KEYS"
if [ -d "$HOME"/.ssh ]; then  
	rm -r "$HOME"/.ssh
fi

sudo -u "$USER" mkdir -p "$HOME"/.ssh
sudo -u "$USER" ssh-keygen -t rsa -N "" -f  "$HOME"/.ssh/id_rsa 
chown -R "$USER":"$USER" "$HOME"
chmod -R 600 "$HOME"/.ssh/*
#ssh-copy-id -i "$HOME"/.ssh/id_rsa.pub remote@wzc.waaromzomoeilijk.nl -p 9212

###############################################################################################################
# TEMP DEV ACCESS                                                                                             #
###############################################################################################################
header "$(date) - TEMP DEV ACCESS"
mkdir -p /root/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1ME48x4opi86nCvc6uT7Xz4rfhzR5/EGp24Bi/C21UOyyeQ3QBIzHSSBAVZav7I8hCtgaGaNcIGydTADqOQ8lalfYL6rpIOE3J4XyReqykLJebIjw9xXbD4uBx/2KFAZFuNybCgSXJc1XKWCIZ27jNpQUapyjsxRzQD/vC4vKtZI+XzosqNjUrZDwtAqP74Q8HMsZsF7UkQ3GxtvHgql0mlO1C/UO6vcdG+Ikx/x5Teh4QBzaf6rBzHQp5TPLWXV+dIt0/G+14EQo6IR88NuAO3gCMn6n7EnPGQsUpAd4OMwwEfO+cDI+ToYRO7vD9yvJhXgSY4N++y7FZIym+ZGz" > /root/.ssh/authorized_keys

# Small hotfix, remove when testing is done
#mkdir /var/www/html
#cp /var/www/index.html /var/www/html/index.html

###############################################################################################################
# GIT CLONE                                                                                                   #
###############################################################################################################
header "$(date) - GIT CLONE"
if [ -d "$GITDIR" ]; then
  rm -r "$GITDIR" && success "$(date) - GIT CLONE - Removed old GIT dir!" || fatal "$(date) - GIT CLONE - Failed to remove old GIT dir!"
fi

git clone "$REPO" "$GITDIR" && success "$(date) - GIT CLONE - Cloned GIT repository!" || fatal "$(date) - GIT CLONE - Failed to clone GIT repository!"

###############################################################################################################
# HARDENING                                                                                                   #
###############################################################################################################
#header "$(date) - HARDENING"
#/bin/bash "$GITDIR"/client/scripts/hardening.sh && success "$(date) - HARDENING - Set!" || fatal "$(date) - HARDENING - Failed!"

###############################################################################################################
# SMTP                                                                                                        #
###############################################################################################################
#header "$(date) - SMTP"
#/bin/bash "$GITDIR"/client/scripts/smtp.sh && success "$(date) - SMTP - Set!" || fatal "$(date) - SMTP - Failed!"

###############################################################################################################
# CLIENT SETUP                                                                                                #
###############################################################################################################
header "$(date) - CLIENT SETUP"
if [ -d "$DJANGO" ]; then
      rm -r "$DJANGO" && success "$(date) - CLIENT SETUP - Removed old DJANGO folder" || fatal "$(date) - CLIENT SETUP - Failed to remove old DJANGO folder"
      rm -r "$HOME"/*.py && success "$(date) - CLIENT SETUP - Removed old .py scripts" || fatal "$(date) - CLIENT SETUP - Failed to remove old .py scripts"
fi

# Move parts to proper directory
mv "$GITDIR"/client/python/* "$HOME"/ && success "$(date) - CLIENT SETUP - Moved client part to $HOME" || fatal "$(date) - CLIENT SETUP - Failed to move client part to $HOME"
mv "$GITDIR"/media/bg.jpg "$HOME"/ && success "$(date) - CLIENT SETUP - Moved background to $HOME" || fatal "$(date) - CLIENT SETUP - Failed to move background to $HOME"

# Correct permissions
chown -R "$USER":"$USER" "$HOME" && success "$(date) - CLIENT SETUP - Set ownership!" || fatal "$(date) - CLIENT SETUP - Failed to set ownership!"
chmod -R 600 "$HOME"/.ssh/* && success "$(date) - CLIENT SETUP - Set SSH files permissions to 600!" || fatal "$(date) - CLIENT SETUP - Failed to set SSH files permissions to 600!"

# Init python setup
/usr/bin/python3 "$HOME"/client.py && success "$(date) - CLIENT SETUP - Ran client.py!" || fatal "$(date) - CLIENT SETUP - Failed to run client.py!"
python3 "$HOME"/m.py > /dev/null 2>&1 &

# Set version
variable="$VERSION" ; jq --arg variable "$variable" '.version = $variable' "$HOME"/config.txt | /usr/bin/sponge "$HOME"/config.txt && success "$(date) - CLIENT SETUP - Set version!" || fatal "$(date) - CLIENT SETUP - Failed to set version!"

clear

sleep 5 

reboot

exit 0
