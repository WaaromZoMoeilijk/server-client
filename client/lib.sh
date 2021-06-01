#!/bin/bash
# Folders
CONFIG="/boot/config.txt"
GITDIR="/var/opt/server-client"
REPO="https://github.com/ezraholm50/server-client" 
DJANGO="/home/pi/pidjango"
TEMPPI="/home/pi"

# System
DEBIAN_FRONTEND="DEBIAN_FRONTEND=noninteractive"
DEBIAN_PRIORITY="DEBIAN_PRIORITY=critical"

# Network
WANIP4=$(curl -s -k -m 5 https://ipv4bot.whatismyipaddress.com)
GATEWAY=$(ip route | grep default | awk '{print $3}')
IFACE=$(ip r | grep "default via" | awk '{print $5}')
ADDRESS=$(hostname -I | cut -d ' ' -f 1)

# Functions
# If script is running as root?
#
# Example:
# if is_root
# then
#     # do stuff
# else
#     print_text_in_color "$IRed" "You are not root..."
#     exit 1
# fi
#
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
    msg_box "Failed, script needs sudo permission"
    exit 1
fi
}

# APT install
apt_install() {
    apt -q4 -y install
}
# APT update
apt_update() {
    apt -qq -d -y update
}
# APT fullupgrade
apt_upgrade() {
    sudo -E apt -qq -d -y -o "Dpkg::Options::=--force-confdef" -o "Dpkg::Options::=--force-confold" full-upgrade
}
# APT autoremove
apt_autoremove() {
    apt -qq -d -y autoremove
}
# APT autoclean
apt_autoclean() {
    apt -qq -d -y autoclean
}

# Spinner during long commands
spinner() {
    printf '['
    while ps "$!" > /dev/null; do
        echo -n '⣾⣽⣻'
        sleep '.7'
    done
    echo ']'
}

# Whiptail 
# auto-size
calc_wt_size() {
    WT_HEIGHT=17
    WT_WIDTH=$(tput cols)

    if [ -z "$WT_WIDTH" ] || [ "$WT_WIDTH" -lt 60 ]; then
        WT_WIDTH=80
    fi
    if [ "$WT_WIDTH" -gt 178 ]; then
        WT_WIDTH=120
    fi
    WT_MENU_HEIGHT=$((WT_HEIGHT-7))
    export WT_MENU_HEIGHT
}

msg_box() {
    [ -n "$2" ] && local SUBTITLE=" - $2"
    whiptail --title "$TITLE$SUBTITLE" --msgbox "$1" "$WT_HEIGHT" "$WT_WIDTH" 3>&1 1>&2 2>&3
}

yesno_box_yes() {
    [ -n "$2" ] && local SUBTITLE=" - $2"
    if (whiptail --title "$TITLE$SUBTITLE" --yesno "$1" "$WT_HEIGHT" "$WT_WIDTH" 3>&1 1>&2 2>&3)
    then
        return 0
    else
        return 1
    fi
}

yesno_box_no() {
    [ -n "$2" ] && local SUBTITLE=" - $2"
    if (whiptail --title "$TITLE$SUBTITLE" --defaultno --yesno "$1" "$WT_HEIGHT" "$WT_WIDTH" 3>&1 1>&2 2>&3)
    then
        return 0
    else
        return 1
    fi
}

input_box() {
    [ -n "$2" ] && local SUBTITLE=" - $2"
    local RESULT && RESULT=$(whiptail --title "$TITLE$SUBTITLE" --nocancel --inputbox "$1" "$WT_HEIGHT" "$WT_WIDTH" 3>&1 1>&2 2>&3)
    echo "$RESULT"
}

input_box_flow() {
    local RESULT
    while :
    do
        RESULT=$(input_box "$1" "$2")
        if [ -z "$RESULT" ]
        then
            msg_box "Input is empty, please try again." "$2"
        elif ! yesno_box_yes "Is this correct? $RESULT" "$2"
        then
            msg_box "OK, please try again." "$2"
        else
            break
        fi
    done
    echo "$RESULT"
}
