#!/bin/bash
# info@waaromzomoeilijk.nl
# login root/raspberry, dietpi/raspberry, pi/raspberry

###################################
# Variables & functions
source <(curl -sL https://raw.githubusercontent.com/ezraholm50/server-client/main/client/lib.sh)

# Check if script runs as root
root_check

###################################
# Update
export "$DEBIAN_FRONTEND"
export "$DEBIAN_PRIORITY"
apt_autoclean
apt_autoremove
apt_update & spinner
apt_upgrade & spinner

###################################
# Dependencies
sudo -E apt -y -o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold" install \
      nano \
      git \
      python3 \
      python3-pip \
      python3-pygame \
      python3-requests \
      python3-setuptools \
      unattended-upgrades \
      openssh-server \
      sshpass \
      net-tools & spinner

sudo -E apt -y -o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold" install \
      libnss-mdns \
      python3-requests \
      avahi-daemon & spinner
      
###################################
# unattended-upgrades
"$DEBIAN_FRONTEND" dpkg-reconfigure unattended-upgrades

###################################
# Temp user, needs a one time password during installation to setup ssh keys.
# Will be replaced with an API mechanism to retrieve clients pub keys.
  rm -r "$TEMPPI"
  echo "Creating user and keys"
  useradd -m -d /home/pi -p $(openssl passwd -crypt raspberry) pi
  usermod -aG sudo pi
  mkdir /home/pi/.ssh
  ssh-keygen -t rsa -N "" -f /home/pi/.ssh/id_rsa 
  chown -R pi:pi /home/pi
  chmod -R 600 /home/pi/.ssh/*
  ssh-copy-id -i /home/pi/.ssh/id_rsa.pub remote@henk.waaromzomoeilijk.nl -p 9212

###################################
# Small hotfix, remove when testing is done
#mkdir /var/www/html
#cp /var/www/index.html /var/www/html/index.html

###################################
# Clone git repo
if [ -d "$GITDIR" ]; then
  rm -r "$GITDIR"
fi

git clone "$REPO" "$GITDIR"

###################################
# Add rc.local
# Add systemd service
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
# Set webserver
# Nginx

###################################
# Hardening
#/bin/bash "$GITDIR"/client/scripts/hardening.sh

###################################
# SSH
#/bin/bash "$GITDIR"/client/scripts/ssh.sh

###################################
# Docker
#/bin/bash "$GITDIR"/client/scripts/docker.sh

###################################
# Overclock
#if cat /proc/cpuinfo | grep -q "Raspberry Pi 4"; then
#     dos2unix "$GITDIR"/client/scripts/overclock.sh
#    /bin/bash "$GITDIR"/client/scripts/overclock.sh
#fi

###################################
# RPI-monitor
#/bin/bash "$GITDIR"/client/scripts/rpi_monitor.sh

###################################
# Nextcloud
#/bin/bash "$GITDIR"/client/scripts/nextcloud.sh

###################################
# SMTP
#/bin/bash "$GITDIR"/client/scripts/smtp.sh

###################################
# Client setup
if [ -d "$DJANGO" ]; then
      echo "Django project exists, removing..."
      rm -r "$DJANGO"
      rm -r "$TEMPPI"/*.py
fi
mv "$GITDIR"/client/python/* "$TEMPPI"/
/usr/bin/python3 "$TEMPPI"/client.py

exit 0
