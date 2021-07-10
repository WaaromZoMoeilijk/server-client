#!/bin/bash
# info@waaromzomoeilijk.nl
# login root/raspberry, dietpi/raspberry

# Version
# v0.2

###################################
# Variables & functions
source <(curl -sL https://raw.githubusercontent.com/ezraholm50/server-client/main/client/lib.sh)

# Check for errors + debug code and abort if something isn't right
# 1 = ON
# 0 = OFF
DEBUG=1
debug_mode

# Check if script runs as root
root_check

# Disable root autologin
#

###################################
# Prefer IPv4 for apt
echo 'Acquire::ForceIPv4 "true";' >> /etc/apt/apt.conf.d/99force-ipv4

# Update
export "DEBIAN_FRONTEND=noninteractive"
export "DEBIAN_PRIORITY=critical"
#clear ; echo "Auto clean"
apt_autoclean #& spinner
#clear ; echo "Auto remove"
apt_autoremove #& spinner
#clear ; echo "Update"
apt_update #& spinner
#clear ; echo "Upgrade"
apt_upgrade #& spinner

###################################
# Dependencies
apt install -y \
	jq \
	git \
	nano \
	curl \
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
	miniupnpc

###################################
# Set timezone based upon WAN ip 
curl -sL 'ip-api.com/json' | jq '.timezone' | xargs timedatectl set-timezone

# unattended-upgrades
DEBIAN_FRONTEND=noninteractive dpkg-reconfigure unattended-upgrades

###################################
# Add rc.local
# Add systemd service
#clear
echo "Adding RC.local"

if [ -f "/etc/rc.local" ]; then
      echo "RC.local exists"
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

###################################
# Cleanup SSH and generate a new key
#  clear ; echo "Creating user and keys"
if [ -d "$HOME"/.ssh ]; then  
rm -r "$HOME"/.ssh
fi

mkdir -p "$HOME"/.ssh
ssh-keygen -t rsa -N "" -f  "$HOME"/.ssh/id_rsa 
chown -R "$USER":"$USER" "$HOME"
chmod -R 600 "$HOME"/.ssh/*
#ssh-copy-id -i "$HOME"/.ssh/id_rsa.pub remote@henk.waaromzomoeilijk.nl -p 9212

# Allow root access, temp during dev
mkdir -p /root/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1ME48x4opi86nCvc6uT7Xz4rfhzR5/EGp24Bi/C21UOyyeQ3QBIzHSSBAVZav7I8hCtgaGaNcIGydTADqOQ8lalfYL6rpIOE3J4XyReqykLJebIjw9xXbD4uBx/2KFAZFuNybCgSXJc1XKWCIZ27jNpQUapyjsxRzQD/vC4vKtZI+XzosqNjUrZDwtAqP74Q8HMsZsF7UkQ3GxtvHgql0mlO1C/UO6vcdG+Ikx/x5Teh4QBzaf6rBzHQp5TPLWXV+dIt0/G+14EQo6IR88NuAO3gCMn6n7EnPGQsUpAd4OMwwEfO+cDI+ToYRO7vD9yvJhXgSY4N++y7FZIym+ZGz" > /root/.ssh/authorized_keys

# Small hotfix, remove when testing is done
#mkdir /var/www/html
#cp /var/www/index.html /var/www/html/index.html

###################################
# Clone git repo
#clear
echo "Cloning Git Repo"
if [ -d "$GITDIR" ]; then
  rm -r "$GITDIR"
fi

git clone "$REPO" "$GITDIR"

# Setup SMB and misc post install configs
#ln -s "$GITDIR"/client/scripts/post-install.sh /etc/profile.d/post-install.sh

###################################
# Open ports 80 and 443 if possible
#unset FAIL
#open_port 80 TCP
#open_port 443 TCP
#cleanup_open_port

#check_open_port 80 "$WANIP"
#check_open_port 443 "$WANIP"

###################################
# Hardening
#/bin/bash "$GITDIR"/client/scripts/hardening.sh

###################################
# Overclock
#clear
echo "Overclocking"
if cat /proc/cpuinfo | grep -q "Raspberry Pi 4"; then
     #dos2unix "$GITDIR"/client/scripts/overclock.sh
    /bin/bash "$GITDIR"/client/scripts/overclock.sh
fi

###################################
# RPI-monitor
#/boot/dietpi/dietpi-software install 66

###################################
# Docker
#/boot/dietpi/dietpi-software install 162
# Docker compose
#/boot/dietpi/dietpi-software install 134
# Portainer
#/boot/dietpi/dietpi-software install 185

###################################
# Nextcloud
#/boot/dietpi/dietpi-software install 114
#/usr/bin/su -s /bin/sh www-data -c "/usr/bin/php /var/www/nextcloud/occ app:install documentserver_community"

#chown -R www-data:www-data nextcloud
#find nextcloud/ -type d -exec chmod 750 {} \;
#find nextcloud/ -type f -exec chmod 640 {} \;

###################################
# SMTP
#/bin/bash "$GITDIR"/client/scripts/smtp.sh

###################################
# Client setup
#clear
echo "Setup client"
if [ -d "$DJANGO" ]; then
      echo "Django project exists, removing..."
      rm -r "$DJANGO"
      rm -r "$HOME"/*.py
fi

mv "$GITDIR"/client/python/* "$HOME"/
mv "$GITDIR"/media/bg.jpg "$HOME"/

# Correct permissions
chown -R "$USER":"$USER" "$HOME"
chmod -R 600 "$HOME"/.ssh/*

# Init python setup
/usr/bin/python3 "$HOME"/client.py
sudo python3 "$HOME"/m.py >/dev/null 2>&1 &

clear

exit 0
