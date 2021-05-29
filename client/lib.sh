#!/bin/bash

CONFIG="/boot/config.txt"
GITDIR="/var/opt/wzm"
REPO="https://github.com/ezraholm50/server-client"  
DJANGO="/home/pi"

WANIP4=$(curl -s -k -m 5 https://ipv4bot.whatismyipaddress.com)
GATEWAY=$(ip route | grep default | awk '{print $3}')
IFACE=$(ip r | grep "default via" | awk '{print $5}')
ADDRESS=$(hostname -I | cut -d ' ' -f 1)

#########################
# Functions
is_root() {
    if [[ "$EUID" -ne 0 ]]
    then
        return 1
    else
        return 0
    fi
}

# Check if root
root_check() {
if ! is_root
then
    echo "Sorry, you are not root."
    exit 1
fi
}

# Generate password
gen_passwd() {
    local length=$1
    local charset="$2"
    local password=""
    while [ ${#password} -lt "$length" ]
    do
        password=$(echo "$password""$(head -c 100 /dev/urandom | LC_ALL=C tr -dc "$charset")" | fold -w "$length" | head -n 1)
    done
    echo "$password"
}

# Check if process is runnnig: is_process_running dpkg
is_process_running() {
PROCESS="$1"

while :
do
    RESULT=$(pgrep "${PROCESS}")

    if [ "${RESULT:-null}" = null ]; then
            break
    else
            print_text_in_color "$ICyan" "${PROCESS} is running, waiting for it to stop."
            sleep 30
    fi
done
}

