![Project layout](/media/projectlayout.png)

## Timeline
- End May Base image ready
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
1. User connects device to Ethernet
2. Either user goes to: domain.local (on local LAN) or connect a monitor to the RPI
  a. From there writes down a registration code (device_ID)
3. Visit register.domain.tld (Button to proceed to registration in browser)
  a. Enter device identifier, username, email and a password. This registers the user and their device.
  b. They get redirected to username.domain.tld (their cloud)
```

## Functionalities user management panel:

Users can visit cloud.domain.tld where they can manage and monitor their new Cloud RPI.

* Monitor: Resources, LAN/WAN IP, Health, Device ID, Uptime, Ping response server/client, Ports used for reverse SSH
* Config: Wifi/ethernet config, hostname, remove node option, notifications
* Webshell
* System config (milestone 2)
* RAID (milestone 2)
* User management (milestone 2)
* Samba/NFS (milestone 3)
* Install various applications to extend functionality (milestone 3)
* Backup/restore (milestone 3)


## Functionalities admin management panel:

Administrators can visit admin.domain.tld where they can manage and monitor all online/offline registered devices.

* Monitor: Resources, LAN/WAN IP, Health, Device ID, Uptime, Ping response server/client, Ports used for reverse SSH of all devices
* Individual system config (milestone 2)
* User management (milestone 2)
* Suspend connection for users/devices (milestone 3)
* Webshell, icon in vertical device info bar per device (milestone 3)

---
At first boot, the users device will contact the server, send network information, computernumber, and expects a device_id back. The device_id is used for registering the user and their device to our server. The device_id + 10000 is the portnr used for reverse SSH. 

Upon registering and email validation on above webui, the client raspberry automatically sets up a reverse SSH (HTTP/HTTPS) connection on (device_id + 10000) port on the server thus enabling us to proxy their website instead of locally portforwarding.

In the background the initial user registration procedure also creates a Nextcloud user with the same credentials. Which for now is an admin (role) for nextcloud until I've found how to integrate usermanagement in the webui. So right after registering the device they can right away use the file storage nextcloud offers. I aim to have these credentials reused by any application we install later on.



