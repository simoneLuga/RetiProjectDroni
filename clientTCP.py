#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 17:27:21 2022

@author: alex
"""

import socket
import threading
import json

 
def reciveMessage():
     try:
         while True:
             packet = json.loads(client.recv(1024).decode())
             #message =  packet.message;
             print("{0} | {1} | {2} | {3} | message: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
     except:
        print("Gateway  2 down")
         

     

         
         

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("localhost", 8062))


thread1 = threading.Thread(target=reciveMessage, args=())
thread1.start()

while True:
    try:
        drone_ip = input("\nDrone_IP : ")
        indirizzo = input("\nIndirizzo destinazione : ")
        
        
        packet = {
                "sourceMAC":"undefined",
                "destinationMAC": "undefined",
                "sourceIP":"undefined",
                "destinationIP":drone_ip,
                "message":indirizzo
            }

        client.send(json.dumps(packet).encode('utf8'))
        
        if indirizzo == "close":
            client.close()
            break
    except: 
        print("Gateway 1 down")
    
    




