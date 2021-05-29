#!/bin/bash
# info@waaromzomoeilijk.nl
###################################
# Variables & functions
source <(curl -sL https://raw.githubusercontent.com/ezraholm50/server-client/main/client/lib.sh)

###################################
# Update
export DEBIAN_FRONTEND=noninteractive
export DEBIAN_PRIORITY=critical
sudo -E apt -qy update
sudo -E apt -qy -o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold" full-upgrade
sudo -E apt -qy autoclean

###################################
# Dependencies
sudo -E apt -qy -o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold" install \
      nano \
      git \
      python3 \
      unattended-upgrades \
      openssh-server

###################################
# unattended-upgrades
dpkg --reconfigure unattended-upgrades

###################################
# Clone git repo or pull latest updates
if [ -d "$GITDIR" ]; then
  cd "$GITDIR" && git pull && cd ~
else  
  git clone "$REPO" "$GITDIR"
fi

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
/bin/bash "$GITDIR"/rpi/scripts/hardening.sh

###################################
# SSH
/bin/bash "$GITDIR"/rpi/scripts/ssh.sh

###################################
# Docker
#/bin/bash "$GITDIR"/rpi/scripts/docker.sh

###################################
# Overclock
if cat /proc/cpuinfo | grep -q "Raspberry Pi 4"; then
    /bin/bash "$GITDIR"/rpi/scripts/overclock.sh
fi

###################################
# RPI-monitor
/bin/bash "$GITDIR"/rpi/scripts/rpi_monitor.sh

###################################
# Nextcloud
/bin/bash "$GITDIR"/rpi/scripts/nextcloud.sh

###################################
# SMTP
/bin/bash "$GITDIR"/rpi/scripts/smtp.sh

###################################
# Client setup
/bin/bash "$GITDIR"/rpi/scripts/setup_client.sh

exit 0
