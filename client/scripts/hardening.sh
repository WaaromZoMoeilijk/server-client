#!/bin/bash

# Setup maintenance/support user
adduser maintenance
usermod -aG sudo maintenance
sudo -u maintenance ssh-keygen

# UFW
apt install ufw -y
ufw default allow outgoing
ufw default deny incoming
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# Fail2ban
# SSH
# Nextcloud
# ?

exit 0
