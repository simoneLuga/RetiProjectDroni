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

#impostare a True se si volgiono visualizzare i log dei pacchetti inviati e ricevuti
printPacket=False

myIP = "0.0.0.0"
myMAC = "D1:00:00:D1"

gatewayMac = "AA:00:00:01"
gatewayIP = "192.168.1.1"

#É impostato statico nel  gateway
ClientIP = "10.10.10.2"

buffer = 1024

DronePort = "8081"

server_address = ('localhost', int(DronePort))

#Funzione che rispone a tutte le richieste : non sono disponibile 
#viene avviata su un thread mentre il drono é in viaggio
def reciveMessage():
    try:
        while True:
            data, address = sock.recvfrom(buffer)
            packet = json.loads(data.decode('utf8'))   
            elapsedTime = time.time() - packet["time"]
            print("\n\trecive from CLIENT:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"])
                  if printPacket else "Recive: "+packet["message"])
            
            newPacket = {
                  "sourceMAC" : myMAC,
                  "destinationMAC" : gatewayMac,
                  "sourceIP" : myIP,
                  "destinationIP" : ClientIP,
                  "message": myIP + " - non sono disponibile",
                  "time": time.time()
              }
            
            print("\n\tsend:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(newPacket["sourceIP"], newPacket["sourceMAC"], newPacket["destinationIP"], newPacket["destinationMAC"], newPacket["message"])
                  if printPacket else "Send: "+newPacket["message"])
            
            newPacket  = json.dumps(newPacket)
            sock.sendto(newPacket.encode(), server_address)     
               
                
    except Exception:        
        print("\nClose socket UDP")     



#Chiediamo al gateway un indirizzo IP
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
    
    print("\n\tsend:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"])
          if printPacket else "\n"+packet["message"])
    packet  = json.dumps(packet)
    sent = sock.sendto(packet.encode(), server_address)
    
    #si mette in attesa di una risopsta dal gateway
    data, server = sock.recvfrom(buffer)
    packet = json.loads(data.decode('utf8'))
    elapsedTime = time.time() - packet["time"]
    print("\n\trecive:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"])
          if printPacket else packet["message"])       
    myIP = packet["destinationIP"]
      
except Exception as info:
    print(info)
finally:
    print("IP address : {}".format(myIP))

#Se ci é stato asseganto un ip ci rendiamo disponibili al volo    
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
        
        print("\n\tsend:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"])
              if printPacket else "Send: "+packet["message"])
        
        #forma il json ed invia
        packet  = json.dumps(packet)
        sent = sock.sendto(packet.encode(), server_address)

        #si mette in attesa di una risopsta dal gateway
        while True:
            data, server = sock.recvfrom(buffer)
            packet = json.loads(data.decode('utf8'))
            elapsedTime = time.time() - packet["time"]
            
            print("\n\trecive:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"])
                  if printPacket else "Recive: "+packet["message"])       
            
            if packet["message"] == "LIST":
                newPacket = {
                      "sourceMAC" : myMAC,
                      "destinationMAC" : gatewayMac,
                      "sourceIP" : myIP,
                      "destinationIP" : ClientIP,
                      "message": "{} - sono disponibile".format(myIP),
                      "time": time.time()
                  }
                print("\n\tsend:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(packet["sourceIP"], newPacket["sourceMAC"], newPacket["destinationIP"], newPacket["destinationMAC"], newPacket["message"])
                      if printPacket else "Send: "+newPacket["message"])
                newPacket  = json.dumps(newPacket)
                sent = sock.sendto(newPacket.encode(), server_address)
                
            else:
                break
            
        #Usciamo dal while per chiudere l esecuzione
        if packet["message"] == "CLOSE":
            break
        
        #Parte
        wait = random.randint(15,20)
        
        
        threadUDPRecive= threading.Thread(target=reciveMessage, args=())
        threadUDPRecive.start()
        
        print("\nIN TRANSITO -> {0}  ...".format(packet["message"]))
        time.sleep(wait)
        
        print("\nCONSEGANTO RITORNO ...")
        
        packet = {
                "sourceMAC" : myMAC,
                "destinationMAC" : gatewayMac,
                "sourceIP" : myIP,
                "destinationIP" : ClientIP,
                "message" : "{0}: PACCO CONSEGNATO in {1}s - torno alla base".format(myIP,wait),
                "time": time.time()
            }
        packet  = json.dumps(packet)
        sent = sock.sendto(packet.encode(), server_address)
        
        #non si aspetta risposta e torna alla base
        time.sleep(wait)  
        print("IN BASE")
        
        
    except Exception as info:
        print(info)
    finally:
        print ('\nClosing socket')
        sock.close()
        
        
        
        
        
        
        