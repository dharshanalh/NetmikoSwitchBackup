#!/usr/bin/python3
###############################
# Written by dharshanalh
# Netmiko and Python 3 based Switch backup Script
# Date: 2020-08-31
# Written for Linux based Operating system
# Tested in Fedora 27
# Supported Switch Models
# Tested with following Models
# HPE Switches 1910 COMWARE 5, 1920 COMWARE 5, 1950 COMWARE 7, 5510 COMWARE 7, 5500 COMWARE 5
# 3COM 2928(HPE1910) COMWARE 5
##############################
import time
from netmiko import Netmiko
import os
import hashlib
##############################################

HP_1910 = {
	"ip": "IP_ADDRESS",
	"username": "USERNAME",
	"password": "PASSWORD",
	"device_type": "hp_comware512900",
}

THREECOM_2928 = {
	"ip": "IP_ADDRESS",
	"username": "USERNAME",
	"password": "PASSWORD",
	"device_type": "hp_comware512900",
}

HP_1920 = {
    "ip": "IP_ADDRESS",
    "username": "USERNAME",
    "password": "PASSWORD",
    "device_type": "hp_comwarejinhua",
}

HP_1950 = {
    "ip": "IP_ADDRESS",
    "username": "USERNAME",
    "password": "PASSWORD",
    "device_type": "hp_comwarefoes",
}

HP_5510 = {
    "ip": "IP_ADDRESS",
    "username": "USERNAME",
    "password": "PASSWORD",
    "device_type": "hp_comware",
}

HP_5500 = {
    "ip": "IP_ADDRESS",
    "username": "USERNAME",
    "password": "PASSWORD",
    "device_type": "hp_comware",
}
###############################################################

sw_list = [HP_1910,THREECOM_2928,HP_1920,HP_1950,HP_5510,HP_5500];


for device in sw_list:
    response = os.system("ping -c 1 " + device['ip']) # check whether the switch is UP using ICMP echo request
    if response == 0:
        print('switch with ip address ', device['ip'],' is UP')
        net_connect = Netmiko(**device)
        print(net_connect.find_prompt())
        print('Initiating backup of : ', device['ip'],' switch')
        output = net_connect.send_command("display cu")
        filename1 = device['ip']
        completeName = filename1 + "_sw.txt" # generate file name
        if os.path.isfile(os.path.join('/PATH/TO/STORE/BACKUP/FILES',completeName)):
            print("######### File Exists #########")
            # open previous backup file
            with open(os.path.join('/PATH/TO/STORE/BACKUP/FILES',completeName),"rb") as f:
                bytes1 = f.read() # read entire previous backup file as bytes
                readable_hash_old = hashlib.sha256(bytes1).hexdigest(); # calculate previous backup hash
                print("Old hash : ",readable_hash_old)
            completeNameTmp = filename1 + "tmp_sw.txt" # generate temporay file name
            with open(os.path.join('/PATH/TO/STORE/BACKUP/FILES',completeNameTmp), 'w') as f:
                print(output, file=f) # write backup to temporay file
            with open(os.path.join('/PATH/TO/STORE/BACKUP/FILES',completeNameTmp),"rb") as f:
                bytes2 = f.read() # read entire new temporay backup file as bytes
                readable_hash_new = hashlib.sha256(bytes2).hexdigest(); # calculate new temporay backup hash
                print("New hash : ",readable_hash_new)
            print(readable_hash_old,' = ',readable_hash_new)
            if readable_hash_old == readable_hash_new:
                os.remove(os.path.join('/PATH/TO/STORE/BACKUP/FILES',completeNameTmp))
                print("New Temporary Backup File Removed!")
            else:
                os.remove(os.path.join('/PATH/TO/STORE/BACKUP/FILES',completeName))
                print("Old Backup File Removed!")
                os.remove(os.path.join('/PATH/TO/STORE/BACKUP/FILES',completeNameTmp))
                print("New Temporary Backup File Removed!")
                with open(os.path.join('/PATH/TO/STORE/BACKUP/FILES',completeName), 'w') as f:
                    print(output, file=f)
                    print("New Backup File Created")
            print('completed backup of : ', device['ip'],'  switch')
            net_connect.disconnect()
        else:
            print("######### New File Created #########")
            with open(os.path.join('/PATH/TO/STORE/BACKUP/FILES',completeName), 'w') as f:
                print(output, file=f)
            print('completed backup of : ', device['ip'],'  switch')	
            net_connect.disconnect()
    else:
        print('switch with ip address ', device['ip'],' is DOWN')

