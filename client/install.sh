#!/bin/bash
# info@waaromzomoeilijk.nl
# login root/raspberry, dietpi/raspberry, pi/raspberry

# Version
# v0.1

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

###################################
# Prefer IPv4 for apt
echo 'Acquire::ForceIPv4 "true";' >> /etc/apt/apt.conf.d/99force-ipv4

# Update
export "$DEBIAN_FRONTEND"
export "$DEBIAN_PRIORITY"
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
	python3 \
	python3-pip \
	python3-pygame \
	python3-requests \
	python3-setuptools \
	unattended-upgrades \
	python3-requests \
	openssh-server \
	avahi-daemon \
	libnss-mdns \
	miniupnpc \
	net-tools \
	sshpass

###################################
# Set timezone based upon WAN ip 
curl -sL 'ip-api.com/json' | jq '.timezone' | xargs timedatectl set-timezone

# unattended-upgrades
"$DEBIAN_FRONTEND" dpkg-reconfigure unattended-upgrades

###################################
# Temp user, needs a one time password during installation to setup ssh keys.
# Will be replaced with an API mechanism to retrieve clients pub keys.
#  clear ; echo "Creating user and keys"
  #rm -r "$TEMPPI"
  #useradd -m -d /home/dietpi -p $(openssl passwd -crypt raspberry) pi
  #usermod -aG sudo pi
  #mkdir /home/dietpi
  rm -r /home/dietpi/.ssh
  mkdir /home/dietpi/.ssh
  ssh-keygen -t rsa -N "" -f /home/dietpi/.ssh/id_rsa 
  chown -R dietpi:dietpi /home/dietpi
  chmod -R 600 /home/dietpi/.ssh/*
  ssh-copy-id -i /home/dietpi/.ssh/id_rsa.pub remote@henk.waaromzomoeilijk.nl -p 9212

# Temp for developing
mkdir -p /root/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC1ME48x4opi86nCvc6uT7Xz4rfhzR5/EGp24Bi/C21UOyyeQ3QBIzHSSBAVZav7I8hCtgaGaNcIGydTADqOQ8lalfYL6rpIOE3J4XyReqykLJebIjw9xXbD4uBx/2KFAZFuNybCgSXJc1XKWCIZ27jNpQUapyjsxRzQD/vC4vKtZI+XzosqNjUrZDwtAqP74Q8HMsZsF7UkQ3GxtvHgql0mlO1C/UO6vcdG+Ikx/x5Teh4QBzaf6rBzHQp5TPLWXV+dIt0/G+14EQo6IR88NuAO3gCMn6n7EnPGQsUpAd4OMwwEfO+cDI+ToYRO7vD9yvJhXgSY4N++y7FZIym+ZGz" > /root/.ssh/authorized_keys

###################################
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

exit 0
EOF

      # Set execute permission
      chmod +x /etc/rc.local

      # Enable service
      systemctl enable rc-local

      # Start service
      systemctl start rc-local
fi

###################################
# Open ports 80 and 443 if possible
#unset FAIL
#open_port 80 TCP
#open_port 443 TCP
#cleanup_open_port

#check_open_port 80 "$WANIP"
#check_open_port 443 "$WANIP"

###################################
# Set webserver
#clear
#echo "Installing Nginx"
# Nginx

###################################
# Hardening
#clear
#echo "Hardening server"
#/bin/bash "$GITDIR"/client/scripts/hardening.sh

###################################
# SSH
#clear
#echo "Securing SSH"
#/bin/bash "$GITDIR"/client/scripts/ssh.sh

###################################
# Docker
#clear
#echo "Installing Docker, compose and Portainer"
#/bin/bash "$GITDIR"/client/scripts/docker.sh

###################################
# Overclock
#clear
#echo "Overclocking"
#if cat /proc/cpuinfo | grep -q "Raspberry Pi 4"; then
#     dos2unix "$GITDIR"/client/scripts/overclock.sh
#    /bin/bash "$GITDIR"/client/scripts/overclock.sh
#fi

###################################
# RPI-monitor
#clear
#echo "Installing RPI-Monitor"
#/bin/bash "$GITDIR"/client/scripts/rpi_monitor.sh

###################################
# Nextcloud
#clear
#echo "Installing Nextcloud"
#/bin/bash "$GITDIR"/client/scripts/nextcloud.sh

###################################
# SMTP
#clear
#echo "Setting up email"
#/bin/bash "$GITDIR"/client/scripts/smtp.sh

###################################
# Client setup
#clear
echo "Setup client"
if [ -d "$DJANGO" ]; then
      echo "Django project exists, removing..."
      rm -r "$DJANGO"
      rm -r "$TEMPPI"/*.py
fi
mv "$GITDIR"/client/python/* "$TEMPPI"/
mv "$GITDIR"/media/bg.jpg "$TEMPPI"/
/usr/bin/python3 "$TEMPPI"/client.py
chown -R dietpi:dietpi /home/dietpi
chmod -R 600 /home/dietpi/.ssh/*
#clear

#sleep 25
#reboot

exit 0
