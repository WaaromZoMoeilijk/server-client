# Server Client
This project enables us to setup a client-server connection and automatic proxy (after registering) to access your personal cloud storage from anywhere without portforwarding. Besides that the device will publish mulitple file servers to accomodate a variaty of platforms to integrate.

This system is modular and can be extended with anything later on. Prebuild software repo's:

[DietPI](https://dietpi.com/docs/software/) | [Linuxserver.io](https://docs.linuxserver.io/) | [Awesome Selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted)

## Timeline
- [x] End May Base image (BETA) ready
- End May / Early June POC server/client
- July Beta 0.1
- ? 1.0

## To do:
- [ ] What are we going to call the project?
- [ ] network drive published (easy & automated)
- [ ] Prefer local connections over proxied connections
- [ ] Functionalities user Web Interface
- [ ] Have a nice material theme for the user Web Interface, current is just a functional design
- [ ] Domain name?
- [ ] Terms of service (milestone 4)
- [ ] Privacy policy (milestone 4)
## Workflow:
```
as easy as possible 

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
- [Download](https://www.balena.io/etcher/) and install Balena Etcher
- [Download client RaspberryPI4 (8GB) (ARMv6)](https://nextcloud.waaromzomoeilijk.nl/s/XRS9ip8eKJQHdSj) | Download client RaspberryPI4 (8GB) (ARMv8) (64Bit)
- Flash the base image to a proper SSD like a [2TB Samsung EVO](https://www.amazon.com/SAMSUNG-Inch-Internal-MZ-77E2T0B-AM/dp/B08QB93S6R/ref=sr_1_1?dchild=1&keywords=samsung+evo+2tb&qid=1622628534&sr=8-1)/[WD RED](https://www.amazon.com/Red-SA500-NAS-NAND-Internal/dp/B07YFGG261/ref=sr_1_3?dchild=1&keywords=wd+nas+2tb+ssd&qid=1622628747&s=electronics&sr=1-3) with a [SATA3 to USB3 adapter](https://www.amazon.com/dp/B00XLAZODE/ref=twister_B07X6JDCVM?_encoding=UTF8&th=1). Or an SDCard reader.

## First boot
- Attach SSD & adapter / SDCard, ethernet and power (optionally a monitor) wait about 25 minutes (SDCard will take a lot longer).
- Open a browser (Mobile/Desktop) and go to http://wzm.local or attatch a monitor and watch the initial installation. 
- A setup screen appears with an activation code once the installation is complete. Could take more then the stated 25 minutes depending on your network connection.
- Follow instructions and on screen urls
- After you have registered you can access your files via 
* USERNAME.waaromzomoeilijk.nl
* Windows network share (Use [option 1](https://www.tenforums.com/tutorials/112017-view-all-network-shares-windows-pc.html) Or use [this](https://www.onmsft.com/how-to/how-to-connect-to-a-network-share-in-windows-10) guide.)

```
Username / Password - Gets set to password used on register.waaromzomoeilijk.nl after device activation.
root      raspberry
dietpi    raspberry
```

## Optional installation options
- On any debian based RaspberryPI4 you could do: `wget https://raw.githubusercontent.com/ezraholm50/server-client/main/client/install.sh && sudo bash install.sh`
- If you are using DietPI you can add this [dietpi.txt](https://raw.githubusercontent.com/ezraholm50/server-client/main/client/dietpi.txt) file to your /boot/ directory

## Functionalities user management panel:

Users can visit https://davecloudserver.waaromzomoeilijk.nl:2021 where they can manage and monitor their new Cloud RPI.

* Monitor: Resources, LAN/WAN IP, Health, Device ID, Uptime, Ping response server/client, Ports used for reverse SSH
* Config: Wifi/ethernet config, hostname, remove node option, notifications
* Webshell
* System config (milestone 2)
* RAID (milestone 2)
* User management (milestone 2)
* Samba 
* Install various applications to extend functionality (milestone 3)
* Backup/restore (milestone 3)


## Functionalities admin management role:

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

![Project layout](/media/projectlayout.png)

