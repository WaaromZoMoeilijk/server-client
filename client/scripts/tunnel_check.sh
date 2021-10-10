#!/bin/bash

if n=$(ss | grep $(host wzc.waaromzomoeilijk.nl | awk {'print $4'}) | grep 9212); then
	echo "Tunnel to backend is active: ${n}"
	exit 0
else
	echo "No reverse SSH tunnels found, connecting"
	ssh -i /home/dietpi/.ssh/id_rsa -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -fNTR $(cat "/home/dietpi/ssh_port"):localhost:80 remote@wzc.waaromzomoeilijk.nl -p 9212 \
	&& exit 0
	echo "Failed to setup tunnel"
	exit 1
fi
