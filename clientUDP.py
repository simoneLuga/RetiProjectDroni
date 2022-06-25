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
server_address = ('localhost', 8063)



while True:
    message = "disponibile"
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    
    try:
        
        packet = {
                "sourceMAC" : myMAC,
                "destinationMAC" :"undefined",
                "sourceIP" : myIP,
                "destinationIP" : "undefined",
                "message": message
            }
        
       
        
        # inviate il messaggio
        print("{0} | {1} | {2} | {3} | message: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
        
        packet  = json.dumps(packet)
        sent = sock.sendto(packet.encode(), server_address)

        # Ricevete la risposta dal server
        #print('Sono disponibile')
        
        data, server = sock.recvfrom(4096)
        packet = json.loads(data.decode('utf8'))
        print("{0} | {1} | {2} | {3} | message: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
        wait = random.randint(5,10)
        time.sleep(wait)
        
        
        
    except Exception as info:
        print(info)
    finally:
        print ('closing socket')
        sock.close()
        
        
        
        
        
        
        