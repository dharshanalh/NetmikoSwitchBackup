#!/usr/bin/python3

###############################
# Written by dharshanalh
# Netmiko and Python 3 based Switch backup Script
# Date: 2020-08-31
# Written for Linux based Operating system
# Tested in Fedora 27
# Supported Switch Models
# Tested with following Models
# HPE 2920 Procurve Switch
# Aruba 2530 Switch
##############################
import time
from netmiko import Netmiko
import os
import hashlib
##############################################

HPE_2920 = {
    "ip": "IP_ADDRESS",
    "username": "USERNAME",
    "password": "PASSWORD",
    "device_type": "hp_procurve",
}

ARUBA_2530 = {
    "ip": "IP_ADDRESS",
    "username": "USERNAME",
    "password": "PASSWORD",
    "device_type": "hp_procurve",
}

##############################################################################

sw_list = [HPE_2920,ARUBA_2530];


for device in sw_list:
    response = os.system("ping -c 1 " + device['ip']) # check whether the switch is UP using ICMP echo request
    if response == 0:
        print('switch with ip address ', device['ip'],' is UP')
        net_connect = Netmiko(**device)
        print(net_connect.find_prompt())
        print('Initiating backup of : ', device['ip'],' switch')
        net_connect.enable()
        output = net_connect.send_command("show running-config")
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

