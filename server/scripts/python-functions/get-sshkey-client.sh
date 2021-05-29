#!/bin/bash
# Get client sshkey to add to .ssh/authorized keys on server
# Username will be set as hostname upon registration
echo "" >> /home/remote/.ssh/authorized_keys                      # (source on client & destination on server)
echo "# Username: $(cat /etc/hostname)" >> /home/remote/.ssh/authorized_keys # (source on client & destination on server)
cat /home/pi/.ssh/id_rsa.pub >> /home/remote/.ssh/authorized_keys # (source on client & destination on server)

exit 0
