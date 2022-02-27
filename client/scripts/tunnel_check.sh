#!/bin/bash

if n=$(ss | grep $(host wzc.waaromzomoeilijk.nl | awk {'print $4'}) | grep 9212); then
	echo "Tunnel to backend is active: ${n}"
	exit 0
else
	echo "No reverse SSH tunnels found, connecting"
	#ssh -i /home/dietpi/.ssh/id_rsa -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -fNTR 8022:localhost:22 remote@wzc.waaromzomoeilijk.nl -p 9212 && echo "Temp SSH tunnel setup" || echo "Failed to setup SSH tunnel"
	ssh -i /home/dietpi/.ssh/id_rsa -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -fNTR $(cat "/home/dietpi/ssh_port"):localhost:80 remote@wzc.waaromzomoeilijk.nl -p 9212 && echo "Nextcloud forwarded via SSH" && exit 0 || echo "Failed to forward Nextcloud via SSH" && exit 1
fi
