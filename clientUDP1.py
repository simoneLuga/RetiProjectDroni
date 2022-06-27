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
import time

myIP = "0.0.0.0"
myMAC = "00:00:00:01"

gatewayMac = "00:00:00:00"
gatewayIP = "192.168.1.1"
buffer = 4096

DronePort = "8081"

server_address = ('localhost', int(DronePort))

try:
    message = "IP address request"
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    
    packet = {
            "sourceMAC" : myMAC,
            "destinationMAC" : gatewayMac,
            "sourceIP" : myIP,
            "destinationIP" : gatewayIP,
            "message": message,
            "time": time.time()
        }
    
    print("\nlog send:\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
    packet  = json.dumps(packet)
    sent = sock.sendto(packet.encode(), server_address)
    
    #si mette in attesa di una risopsta dal gateway
    data, server = sock.recvfrom(buffer)
    packet = json.loads(data.decode('utf8'))
    elapsedTime = time.time() - packet["time"]
    print("\nlog revice:\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nTime elapsed: {4}\nmessage: {5}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime, packet["message"]))
    
    myIP = packet["destinationIP"]
    
    
except Exception as info:
    print(info)
finally:
    print ('closing socket')
    print("IP address : {}".format(myIP))
    sock.close()
    
while myIP != "0.0.0.0":
    
    message = "disponibile"
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    
    try:
        
        packet = {
                "sourceMAC" : myMAC,
                "destinationMAC" : gatewayMac,
                "sourceIP" : myIP,
                "destinationIP" : gatewayIP,
                "message": message,
                "time": time.time()
            }
        # inviate il messaggio
        print("\nlog send:\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
        
        #forma il json ed invia
        packet  = json.dumps(packet)
        sent = sock.sendto(packet.encode(), server_address)
        
        #si mette in attesa di una risopsta dal gateway
        data, server = sock.recvfrom(buffer)
        packet = json.loads(data.decode('utf8'))
        elapsedTime = time.time() - packet["time"]
        print("\nlog revice:\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nTime elapsed: {4}\nmessage: {5}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime, packet["message"]))
        
        #Parte
        wait = random.randint(1,5)
        print("\n IN TRANSITO...")
        time.sleep(wait)
        
        print("CONSEGANTO RITORNO...")
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
        
        
        
        
        
        
        