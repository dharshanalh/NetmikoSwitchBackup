#!/usr/bin/python3
###############################
# Written by dharshanalh
# Netmiko and Python 3 based Switch backup Script
# Date: 2020-08-31
# Written for Linux based Operating system
# Tested in Fedora 27
# Supported Aruba Controller Models
# Tested with following Models
# Aruba WLAN Controller 7030 7010 7005
##############################

# ARUBA WLAN Controller 7030 7010 7005
##############################
import time
from netmiko import Netmiko
import os
#import hashlib
##############################################

ARUBA_7005 = {
    "ip": "IP_ADDRESS",
    "username": "USERNAME",
    "password": "PASSWORD",
    "secret": "ENABLE_PASSWORD",
    "device_type": "cisco_ios",
}

ARUBA_7010 = {
    "ip": "IP_ADDRESS",
    "username": "USERNAME",
    "password": "PASSWORD",
    "secret": "ENABLE_PASSWORD",
    "device_type": "cisco_ios",
}

ARUBA_7030 = {
    "ip": "IP_ADDRESS",
    "username": "USERNAME",
    "password": "PASSWORD",
    "secret": "ENABLE_PASSWORD",
    "device_type": "cisco_ios",
}

sw_list = [ARUBA_7005,ARUBA_7010,ARUBA_7030];


for device in sw_list:
    response = os.system("ping -c 1 " + device['ip']) # check whether the switch is UP using ICMP echo request
    if response == 0:
        print('WLAN Controller with ip address ', device['ip'],' is UP')
        net_connect = Netmiko(**device)
        print(net_connect.find_prompt())
        print('Initiating backup of : ', device['ip'],' WLAN Controller')
        #net_connect.enable()
        #print(net_connect.find_prompt())
        net_connect.write_channel('no paging')
        output = net_connect.send_command("show running-config")
        filename1 = time.strftime("%Y%m%d-%H%M%S")
        filename2 = device['ip']
        completeName = filename2 + "_" + filename1 + "_cont.txt"
        with open(os.path.join('/PATH/TO/STORE/BACKUP/FILES',completeName), 'w') as f:
            print(output, file=f)
        print('completed backup of : ', device['ip'],' WLAN Controller')	
        net_connect.disconnect()
    else:
        print('WLAN Controller with ip address ', device['ip'],' is DOWN')

