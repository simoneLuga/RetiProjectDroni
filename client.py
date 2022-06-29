#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Presepi Alex - 0000976898
alex.presepi@studio.unibo.it
Lugaresi Simone - 0000970392
simone.lugaresi@studio.unibo.it
"""


import socket
import threading
import json
import time
import sys

printPacket = False

myIP = "0.0.0.0"
myMAC = "CC-CC-CC-00-00-01"

gatewayIP = "10.10.10.1"
gatewayMac = "AA-AA-AA-00-00-00"

broadcastNewtworkDrone = "192.168.1.255"

buffer = 1024
gatewayPort = "8080"
 
def reciveMessage():
     try:
         while True:
             data = client.recv(buffer)
             data = (data.decode()).split('{')
             
             # il primo elemento é nullo causato dallo split
             data.pop(0) 
             for item in data:
                 tempPacket = json.loads("{" + item)
                 elapsedTime = time.time() - tempPacket["time"]
                 print("\n\trecive:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nmessage: {5}".format(tempPacket["sourceIP"], tempPacket["sourceMAC"], tempPacket["destinationIP"], tempPacket["destinationMAC"], elapsedTime,tempPacket["message"]) 
                       if printPacket else tempPacket["message"])
                 
     except:
        print("Close socket")



try:
    #apre la connessione
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", int(gatewayPort)))
    message = "IP address request"
    packet = {
            "sourceMAC":myMAC,
            "destinationMAC": gatewayMac,
            "sourceIP":myIP,
            "destinationIP":gatewayIP,
            "message": message,
            "time": time.time()}
    client.send(json.dumps(packet).encode('utf8'))
    print("\n\tsend:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"])
          if printPacket else "\n"+packet["message"])
    data = client.recv(buffer)
    packet = json.loads(data.decode())
    elapsedTime = time.time() - packet["time"]
    print("\n\trecive:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"])
          if printPacket else packet["message"])       
    myIP = packet["destinationIP"]
    
except: 
    print("Gateway down")
finally:
    print("IP address : {}".format(myIP))

#avvia il thread sullaricezione
thread1 = threading.Thread(target=reciveMessage, args=())
thread1.start()

strHelp=("\nMENU\nLIST > stampa IP lista dei droni disponibili per un nuovo invio di pacchetto" +
       "\nCLOSE > Chiude tutto" +
       "\noppure inserisc lip del drone che vuoi far partire" +
       "\nhelp > stampa la lista dei comandi\n")
print(strHelp)
while True:
    try:
        cmdOrIP = input("\nComando o IPDrone : ")
        packet = {
                "sourceMAC":myMAC,
                "destinationMAC": gatewayMac,
                "sourceIP":myIP}
        
        if cmdOrIP == "help":
            print(strHelp)
        else:
            if cmdOrIP == "LIST" or cmdOrIP == "CLOSE":
                packet["destinationIP"] = broadcastNewtworkDrone
                packet["message"] = cmdOrIP
            else:
                indirizzo = input("Destinazione : ")
                packet["destinationIP"] = cmdOrIP
                packet["message"] = indirizzo
            packet["time"]= time.time()
            client.send(json.dumps(packet).encode('utf8'))
            print("\n\tsend:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"])
                  if printPacket else "")
        if cmdOrIP == "CLOSE":
            client.close()
            break
    except: 
        print("Gateway down")
    
print("By.")    




