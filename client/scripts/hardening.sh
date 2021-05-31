#!/bin/bash

# SSH keys
/bin/rm /etc/ssh/ssh_host_*
/bin/rm /root/.ssh/id_rsa
/bin/rm /root/.ssh/id_rsa.pub
/bin/rm /home/dietpi/.ssh/id_rsa
/bin/rm /home/dietpi/.ssh/id_rsa.pub

dpkg-reconfigure openssh-server

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
