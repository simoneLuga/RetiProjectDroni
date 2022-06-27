#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 17:27:21 2022

@author: alex
"""

import socket
import threading
import json

myIP = "0.0.0.0"
myMAC = "00:00:00:11"

gatewayIP = "10.10.10.1"
gatewayMac = "00:00:00:00"

buffer = 4096

ClientPort = "8080"
 
def reciveMessage():
     try:
         while True:
             packet = json.loads(client.recv(buffer).decode())
             print("log\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
     except:
        print("Gateway  2 down")

#apre la connessione
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", int(ClientPort)))

try:
    message = "IP address request"
    packet = {
            "sourceMAC":myMAC,
            "destinationMAC": gatewayMac,
            "sourceIP":myIP,
            "destinationIP":gatewayIP,
            "message": message}
    client.send(json.dumps(packet).encode('utf8'))
    packet = json.loads(client.recv(buffer).decode())
    print("log\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
    myIP = packet["destinationIP"]
    
except: 
    print("Gateway 1 down")
finally:
    print("IP address : {}".format(myIP))

#avvia il thread sullaricezione
thread1 = threading.Thread(target=reciveMessage, args=())
thread1.start()

print("LIST > stampa IP lista dei droni disponibili per un nuovo invio di pacchetto" +
       "\nCLOSE > Chiude tutto" +
       "\noppure inserisc lip del drone che vuoi far partire" +
       "\nhelp > stampa la lista dei comandi")


    
while True:
    try:
        cmdOrIP = input("\nComando o IPDrone : ")
        
        if cmdOrIP == "help":
            print("LIST > stampa IP lista dei droni disponibili per un nuovo invio di pacchetto" +
                  "\nCLOSE > Chiude tutto" +
                  "\noppure inserisc lip del drone che vuoi far partire" +
                  "\nhelp > stampa la lista dei comandi")
        else:
            if cmdOrIP == "LIST":
                packet = {
                        "sourceMAC":myMAC,
                        "destinationMAC": gatewayMac,
                        "sourceIP":myIP,
                        "destinationIP":gatewayIP,
                        "message": "LIST"}
            elif cmdOrIP == "CLOSE":
                packet = {
                        "sourceMAC":myMAC,
                        "destinationMAC": gatewayMac,
                        "sourceIP":myIP,
                        "destinationIP":gatewayIP,
                        "message": "CLOSE"}
            else:
                indirizzo = input("Indirizzo destinazione : ")
                packet = {
                            "sourceMAC":myMAC,
                            "destinationMAC": gatewayMac,
                            "sourceIP":myIP,
                            "destinationIP":cmdOrIP,
                            "message":indirizzo
                        }
            client.send(json.dumps(packet).encode('utf8'))
            if cmdOrIP == "CLOSE":
                client.close()
                break
        if cmdOrIP == "CLOSE":
            client.close()
            break
    except: 
        print("Gateway 1 down")
    
    




