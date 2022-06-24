#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 17:27:21 2022

@author: alex
"""

import socket
import threading


 
def reciveMessage():
     try:
         while True:
             message = client.recv(1024)
             print(message)
     except:
        print("Gateway down")
         

     

         
         

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("localhost", 8083))
client.send("bello".encode())

thread1 = threading.Thread(target=reciveMessage, args=())
thread1.start()

while True:
    try:
        x = input("Message to send : ")
        client.send(x.encode())
        if x == "close":
            client.close()
            break
    except: 
        print("Gateway down")