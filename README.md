![Project layout](/media/projectlayout.png)

## Timeline
- [x] End May Base image (BETA) ready
- End May / Early June POC server/client
- July Beta 0.1
- ? 1.0

## To do:
- [ ] What are we going to call the project?
- [ ] Domain name?
- [ ] Terms of service (milestone 3)
- [ ] Privacy policy (milestone 3)

## Workflow:
```
1. User connects device to Ethernet and powers it on
2. Automated installation begins and takes about 15 minutes. (Setup screen is shown via HDMI and WEB: http://wzm.local)
2. Either user goes to: http://wzm.local (on local LAN) or connect a monitor to the RPI
  a. From there writes down the activation code and device ID
3. Visit https://register.waaromzomoeilijk.nl:2021/xx/register
  a. Enter Name, username (Userid), email and a password.
  b. Verify by email and login
  c. Register your device
```

# Installation
Base image - [client RaspberryPI4 (8GB) (ARMv6)](https://nextcloud.waaromzomoeilijk.nl/s/Fq5NemfnGmJsXKz)
```
Username / Password - Gets set to password used on register.waaromzomoeilijk.nl after device activation.
root      raspberry
dietpi    raspberry
pi        raspberry
```
Base image - client RaspberryPI4 (8GB) (ARMv8) (64Bit)

This project uses an SSD as main storage on the RPI4, instead of an SDCard.

In order for this to work please execute the following before doing anything else:
## Prepare RPI for SSD boot
- [Download](https://www.raspberrypi.org/downloads) Raspberry Pi Imager 
- Select a spare SD card. The contents will get overwritten!
- Launch Raspberry Pi Imager
- Select Misc utility images under Operating System
- Select Bootloader
- Select boot-mode USB
- Select SD card and then Write
- Boot the Raspberry Pi with the new image and wait for at least 10 seconds.
- The green activity LED will blink with a steady pattern and the HDMI display will be green on success.
- Power off the Raspberry Pi and remove the SD card.

## Flash base image to SSD / SDCard
- [Download](https://www.balena.io/etcher/) Balena Etcher
- Flash the base image to a proper SSD like a 1TB+ Samsung EVO/WD green with a STA3 to USB3 adapter. Or an SDCard reader.

## First boot
- Attach SSD adapter / SDCard, ethernet and power (optionally a monitor) wait 15 minutes (SDCard will take up to an hour).
- Open a browser (Mobile/Desktop) and go to http://wzm.local or attatch a monitor and watch the initial installation. 
- A setup screen appears with an activation code once the installation is complete. Could take 30 minutes depending on your network connection.
- Follow instructions

## Optional installation options
- On any debian based RaspberryPI4 you could do: `wget https://raw.githubusercontent.com/ezraholm50/server-client/main/client/install.sh && sudo bash install.sh`
- If you are using DietPI you can add this [dietpi.txt](https://raw.githubusercontent.com/ezraholm50/server-client/main/client/dietpi.txt) file to your /boot/ directory (This is how the base image works)

## Functionalities user management panel:

Users can visit https://davecloudserver.waaromzomoeilijk.nl:2021 where they can manage and monitor their new Cloud RPI.

* Monitor: Resources, LAN/WAN IP, Health, Device ID, Uptime, Ping response server/client, Ports used for reverse SSH
* Config: Wifi/ethernet config, hostname, remove node option, notifications
* Webshell
* System config (milestone 2)
* RAID (milestone 2)
* User management (milestone 2)
* Samba/NFS (milestone 3)
* Install various applications to extend functionality (milestone 3)
* Backup/restore (milestone 3)


## Functionalities admin management users:

Administrators can visit https://davecloudserver.waaromzomoeilijk.nl:2021 where they can manage and monitor all online/offline registered devices.

* Monitor: Resources, LAN/WAN IP, Health, Device ID, Uptime, Ping response server/client, Ports used for reverse SSH of all devices
* Individual system config (milestone 2)
* User management (milestone 2)
* Suspend connection for users/devices (milestone 3)
* Webshell, icon in vertical device info bar per device (milestone 3)

---
At first boot, the users device will contact the server, send network information, computernumber, and expects a device_id back. The device_id is used for registering the user and their device to our server. The device_id + 10000 is the portnr used for reverse SSH. 

Upon registering and email validation on above webui, the client raspberry automatically sets up a reverse SSH (HTTP/HTTPS) connection on (device_id + 10000) port on the server thus enabling us to proxy their website instead of locally portforwarding.

In the background the initial user registration procedure also creates a Nextcloud user with the same credentials. Which for now is an admin (role) for nextcloud until I've found how to integrate usermanagement in the webui. So right after registering the device they can right away use the file storage nextcloud offers. I aim to have these credentials reused by any application we install later on.



