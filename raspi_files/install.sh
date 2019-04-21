#!/bin/bash

echo '--------------------------------------------'
echo 'Set up us keyboard'
echo 'setxkbmap us' >> /home/pi/.bashrc

sudo apt-get update

sudo apt-get -y install htop

## Set up to create ad hoc network if needed and serve website
# DHCP server
echo '--------------------------------------------'
echo 'Set up DHCP server'
sudo apt-get -y install isc-dhcp-server 
sudo systemctl disable isc-dhcp-server
sudo echo 'ddns-update-style interim;
default-lease-time 600;
max-lease-time 7200;
authoritative;
log-facility local7;
subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.5 192.168.1.150;
}' > /etc/dhcp/dhcpd.conf

# adhoc network configuration
echo '--------------------------------------------'
echo 'set up ad hoc config files'
sudo cp /etc/network/interfaces /etc/network/interfaces-wifi
sudo echo 'auto lo
iface lo inet loopback
iface eth0 inet dhcp

auto wlan0
iface wlan0 inet static
  address 192.168.1.1
  netmask 255.255.255.0
  wireless-channel 1
  wireless-essid RPiwireless
  wireless-mode ad-hoc' > /etc/network/interfaces-adhoc

# Systemd file to check connection upon start up and if it doesn't work reboot and switch to ad hoc
sudo echo '[Unit]
Description=Check whether connected at startup
After=networking.service

[Service]
User=root
ExecStart=/bin/bash /home/pi/check_connection.sh

[Install]
WantedBy=multi-user.target' > /etc/systemd/system/check_connection.service

sudo systemctl enable check_connection


# To serve website and communicate with genesi.gr
echo '--------------------------------------------'
echo 'install tornado and wifi packages'
sudo apt-get -y install python3-tornado
sudo pip3 install wifi websocket-client

echo '--------------------------------------------'
echo 'setup webserver and communication files'
# systemd file for server
sudo echo '[Unit]
Description=Serve a configuration website
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/bin/python3 /home/pi/pi_server.py
Restart=on-failure

[Install]
WantedBy=multi-user.target' > /etc/systemd/system/config_server.service

sudo systemctl enable config_server.service

## Controlling the car remotely
sudo echo "[Unit]
Description=Run a tornado server to communicate with genesi.gr
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/bin/python3 /home/pi/genesi_raspi_car_server.py $1
Restart=always

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/car_server.service
sudo systemctl enable car_server.service
