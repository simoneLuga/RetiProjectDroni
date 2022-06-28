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
import threading

myIP = "0.0.0.0"
myMAC = "00:00:00:01"

gatewayMac = "00:00:00:00"
gatewayIP = "192.168.1.1"

ClientIP = "10.10.10.2"

buffer = 1024

DronePort = "8081"

server_address = ('localhost', int(DronePort))


def reciveMessage(sock):
    while True:
        try:
            data, address = sock.recvfrom(buffer)
            packet = json.loads(data.decode('utf8'))   
            elapsedTime = time.time() - packet["time"]
            print("\n\trecive from CLIENT:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"]))       
            if packet["message"] == "LIST":
                newPacket = {
                      "sourceMAC" : myMAC,
                      "destinationMAC" : gatewayMac,
                      "sourceIP" : myIP,
                      "destinationIP" : ClientIP,
                      "message": myIP + " - non sono disponibile",
                      "time": time.time()
                  }
                newPacket  = json.dumps(packet)
                sent = sock.sendto(newPacket.encode(), server_address)  
        except Exception:        
            print("\nGateway -> close socket UDP")     




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
    
    message = myIP + " - sono disponibile"
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    print ('\nOpen socket')
    try:       
        packet = {
                "sourceMAC" : myMAC,
                "destinationMAC" : gatewayMac,
                "sourceIP" : myIP,
                "destinationIP" : ClientIP,
                "message": message,
                "time": time.time()
            }
        # inviate il messaggio
        print("\n\tsend:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
        
        #forma il json ed invia
        packet  = json.dumps(packet)
        sent = sock.sendto(packet.encode(), server_address)
        print(str(sent) + "sent")
        #si mette in attesa di una risopsta dal gateway
        print("prima aspettp")
        while True:
            print("aspettp")
            data, server = sock.recvfrom(buffer)
            print("dopo")
            packet = json.loads(data.decode('utf8'))
            elapsedTime = time.time() - packet["time"]
            print("\n\trecive:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"]))       
            if packet["message"] == "LIST":
                newPacket = {
                      "sourceMAC" : myMAC,
                      "destinationMAC" : gatewayMac,
                      "sourceIP" : myIP,
                      "destinationIP" : ClientIP,
                      "message": myIP + " - sono disponibile",
                      "time": time.time()
                  }
                newPacket  = json.dumps(packet)
                sent = sock.sendto(newPacket.encode(), server_address)
            else:
                break
            
        if packet["message"] == "CLOSE":
            print("CLOSE")
            break
        #Parte
        wait = random.randint(15,20)
        threadUDPRecive= threading.Thread(target=reciveMessage, args=(sock))
        threadUDPRecive.start()
        print("\nIN TRANSITO...")
        time.sleep(wait)
        print("\nCONSEGANTO RITORNO...")
        #sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        packet["message"] = "PACCO CONSEGNATO in {}s - torno alla base".format(wait)
        packet  = json.dumps(packet)
        sent = sock.sendto(packet.encode(), server_address)
        #non si aspetta risposta e torna alla base
        time.sleep(wait)      
        threadUDPRecive.stop()
    except Exception as info:
        print(info)
    finally:
        print ('\nClosing socket')
        sock.close()
        
        
        
        
        
        
        