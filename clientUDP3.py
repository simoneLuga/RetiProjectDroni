#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 20:42:15 2022

@author: Alex e Simone
"""

import socket as sk
import time
import sys
import json
import random

myIP = "0.0.0.0"
myMAC = "00:00:00:03"

gatewayMac = "00:00:00:00"
gatewayIP = "192.168.1.1"
buffer = 1024

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
    
    print("\n\tsend:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
    packet  = json.dumps(packet)
    sent = sock.sendto(packet.encode(), server_address)
    
    #si mette in attesa di una risopsta dal gateway
    data, server = sock.recvfrom(buffer)
    packet = json.loads(data.decode('utf8'))
    elapsedTime = time.time() - packet["time"]
    print("\n\trecive:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"]))       
    myIP = packet["destinationIP"]
    
    
except Exception as info:
    print(info)
finally:
    print("IP address : {}".format(myIP))
    sock.close()
    
while myIP != "0.0.0.0":
    
    message = "disponibile"
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    print ('\nOpen socket')
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
        print("\n\tsend:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
        
        #forma il json ed invia
        packet  = json.dumps(packet)
        sent = sock.sendto(packet.encode(), server_address)
        
        #si mette in attesa di una risopsta dal gateway
        data, server = sock.recvfrom(buffer)
        packet = json.loads(data.decode('utf8'))
        elapsedTime = time.time() - packet["time"]
        print("\n\trecive:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"]))       
        if packet["message"] == "CLOSE":
            print("CLOSE")
            break
        #Parte
        wait = random.randint(10,15)
        print("\nIN TRANSITO...")
        time.sleep(wait)
        print("\nCONSEGANTO RITORNO...")
        sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        packet["message"] = "PACCO CONSEGNATO in {}s - torno alla base".format(wait)
        packet  = json.dumps(packet)
        sent = sock.sendto(packet.encode(), server_address)
        #non si aspetta risposta e torna alla base
        time.sleep(wait)      
        
    except Exception as info:
        print(info)
    finally:
        print ('\nClosing socket')
        sock.close()
        
        
        
        
        
        
        