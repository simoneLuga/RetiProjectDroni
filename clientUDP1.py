#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 20:42:15 2022

@author: alex
"""

import socket as sk
import time
import json
import random

myIP = "192.168.1.2"
myMAC = "00:00:00:01"

gatewayMac = "00:00:00:00"
gatewayIP = "10.10.10.1"
buffer = 4096

DronePort = "8071"

server_address = ('localhost', int(DronePort))


while True:
    message = "disponibile"
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    
    try:
        
        packet = {
                "sourceMAC" : myMAC,
                "destinationMAC" : gatewayMac,
                "sourceIP" : myIP,
                "destinationIP" : gatewayIP,
                "message": message
            }
        # inviate il messaggio
        print("log\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
        
        #forma il json ed invia
        packet  = json.dumps(packet)
        sent = sock.sendto(packet.encode(), server_address)
        
        #si mette in attesa di una risopsta dal gateway
        data, server = sock.recvfrom(buffer)
        packet = json.loads(data.decode('utf8'))
        print("log\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
        
        #Parte
        wait = random.randint(5,10)
        time.sleep(wait)
        
        
        sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        packet["message"] = "PACCO CONSEGNATO in {}s - torno alla base".format(wait)
        packet  = json.dumps(packet)
        sent = sock.sendto(packet.encode(), server_address)
        #non si aspetta risposta e torna alla base
        time.sleep(wait)      
    except Exception as info:
        print(info)
    finally:
        print ('closing socket')
        sock.close()
        
        
        
        
        
        
        