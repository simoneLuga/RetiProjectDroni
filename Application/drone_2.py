#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Presepi Alex - 0000976898
alex.presepi@studio.unibo.it
Lugaresi Simone - 0000970392
simone.lugaresi@studio.unibo.it
"""


import socket as sk
import time
import sys
import json
import random
import threading

#impostare a True se si volgiono visualizzare i log dei pacchetti inviati e ricevuti
printPacket=False
value = input("Per Debug inserire 1: ")
if value=="1": printPacket=True

minSec = 15
maxSec = 20

myIP = "0.0.0.0"
myMAC = "DD-DD-DD-00-00-02"

gatewayMac = "AA-AA-AA-00-00-00"
gatewayIP = "192.168.1.1"

#É impostato statico nel  gateway
ClientIP = "10.10.10.2"

buffer = 1024
gatewayPort = "8081"
server_address = ('localhost', int(gatewayPort))

state = True #True disponibile , False occupato
   

def shipment(indirizzo, sock):
    #Parte
    global state
    wait = random.randint(minSec,maxSec)
    
    
    
    print("\nIN TRANSITO -> {0}  ...\n".format(indirizzo))
    packet = {
            "sourceMAC" : myMAC,
            "destinationMAC" : gatewayMac,
            "sourceIP" : myIP,
            "destinationIP" : ClientIP,
            "message" : "{0}: Drone partito".format(myIP),
            "time": time.time()
        }
    packet  = json.dumps(packet)
    sock.sendto(packet.encode(), server_address)
    time.sleep(wait)    
    print("\nHO CONSEGNATO, RITORNO ...\n")
    packet = {
            "sourceMAC" : myMAC,
            "destinationMAC" : gatewayMac,
            "sourceIP" : myIP,
            "destinationIP" : ClientIP,
            "message" : "{0}: PACCO CONSEGNATO in {1}s - torno alla base".format(myIP,wait),
            "time": time.time()
        }
    packet  = json.dumps(packet)
    sock.sendto(packet.encode(), server_address) 
    #non si aspetta risposta e torna alla base
    time.sleep(wait)
    print("\nIN BASE\n")
    state = True
    
    available()

def available():
    message = myIP + " - sono disponibile"
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
        sock.sendto(packet.encode(), server_address)
    except:
        print("errore invio messagiigo")
    
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
    print("\n\treceive:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"])
          if printPacket else packet["message"])       
    myIP = packet["destinationIP"]
      
except Exception as info:
    print(info)
finally:
    print("IP address : {}".format(myIP))

#Se ci é stato asseganto un ip ci rendiamo disponibili al volo    
while myIP != "0.0.0.0":
    #
    try:       
        if state: available()
        
        #si mette in attesa di una risopsta dal gateway
        while True:
            data, server = sock.recvfrom(buffer)
            packet = json.loads(data.decode('utf8'))
            elapsedTime = time.time() - packet["time"]
            
            print("\n\treceive:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"])
                  if printPacket else "Receive: "+packet["message"])       
            
            msg = packet["message"]
            if msg == "LIST" or (state==False and msg!="CLOSE"):
                newPacket = {
                      "sourceMAC" : myMAC,
                      "destinationMAC" : gatewayMac,
                      "sourceIP" : myIP,
                      "destinationIP" : ClientIP,
                      "message":  myIP + (" - sono disponibile" if state else " - non sono disponibile"),
                      "time": time.time()
                  }
                print("\n\tsend:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(packet["sourceIP"], newPacket["sourceMAC"], newPacket["destinationIP"], newPacket["destinationMAC"], newPacket["message"])
                      if printPacket else "Send: "+newPacket["message"])
                newPacket  = json.dumps(newPacket)
                sent = sock.sendto(newPacket.encode(), server_address)
            else:
                break
            
        #Usciamo dal while per chiudere l esecuzione
        if msg == "CLOSE":
            break
        
        #Parte la spedizione
        if state:
            state  = False
            threadShip= threading.Thread(target=shipment, args=[packet["message"],sock])
            threadShip.start()

    except Exception as info:
        print(info)

try:
    threadShip.join()
except:
    print("Drone non in spedizione")
finally:
   sock.close()
   print ('\nClosing.')
   sys.exit(0)
    

        
        

     
        
        
        