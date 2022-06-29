#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@authors: Presepi Alex - 0000976898
alex.presepi@studio.unibo.it
Lugaresi Simone - 0000970392
simone.lugaresi@studio.unibo.it
"""

import socket as sk
import json
import threading
import sys
import signal
import ipaddress as ipaddr
import time

packet=""

buffer = 1024

myMAC = "AA-AA-AA-00-00-00"

arp_table_address_droni = {}
arp_table_mac_droni = {}

networkDroni = "192.168.1.0/24"
networkClient = "10.10.10.0/24"

interfaceClientIP = "10.10.10.1"
interfaceClientPort = "8080"

interfaceDroneIP = "192.168.1.1"
interfaceDronePort = "8081"
broadcast = "192.168.1.255"

# IP statico per il client
ClientIP = "10.10.10.2"
ClientMac = "CC-CC-CC-00-00-01"

#inizilize sock
socketUDP = None

def get_ip_from_mac(d, mac):  
    return [k for k, v in d.items() if v == mac]

def assignmentIP(macAddress, address):
    ip = get_ip_from_mac(arp_table_mac_droni, macAddress)
    if len(ip)==0:
        for addr in ipaddr.IPv4Network(networkDroni):
        
            if str(addr) not in arp_table_mac_droni.keys() and str(addr)!= interfaceDroneIP and str(addr)!="192.168.1.0":
                ip =  str(addr)
                arp_table_mac_droni[ip] = macAddress
                break
    else:
        ip = ip[0]
    
    #if ip not in arp_table_address_droni.keys():
    arp_table_address_droni[ip] = address
    newPacket = {
            "sourceMAC":myMAC,
            "destinationMAC":arp_table_mac_droni[ip],
            "sourceIP":interfaceDroneIP,
            "destinationIP":ip,
            "message": "IP assegnato",
            "time": time.time()
        }
    sendUDP(newPacket)    

         
def reciveUDP():
    global socketUDP
    socketUDP = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    server_address = ('localhost', int(interfaceDronePort))
    socketUDP.bind(server_address)
    try:
        while True:
            data, address = socketUDP.recvfrom(buffer)
            packet = json.loads(data.decode('utf8'))   
            elapsedTime = time.time() - packet["time"]
            print("\n\trecive from DRONE:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"]))       
            if packet["message"] == "IP address request":
                assignmentIP(packet["sourceMAC"], address)  
            else:
                arp_table_address_droni[packet["sourceIP"]] = address
                sendTCP(packet)
    except Exception:   
        print("\nGateway -> close socket UDP")
    
def sendUDP(packet):
    newPacket = {
            "sourceMAC":myMAC,
            "sourceIP":interfaceDroneIP,
            "destinationIP":packet["destinationIP"],
            "message": packet["message"],
            "time": time.time()
        } 
    
    try:
        if packet["destinationIP"] == broadcast:
            newPacket["destinationMAC"] = "ff:ff:ff:ff:ff:ff"
            print("\n\tsend to DRONE:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(newPacket["sourceIP"], newPacket["sourceMAC"], newPacket["destinationIP"], newPacket["destinationMAC"], newPacket["message"]))

            for address in arp_table_address_droni.values():
                    socketUDP = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
                    socketUDP.sendto(json.dumps(newPacket).encode('utf8'), address)
                    socketUDP.close()              
        elif packet["destinationIP"] in arp_table_mac_droni.keys():
            newPacket["destinationMAC"] = arp_table_mac_droni[newPacket["destinationIP"]]
            print("\n\tsend to DRONE:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(newPacket["sourceIP"], newPacket["sourceMAC"], newPacket["destinationIP"], newPacket["destinationMAC"], newPacket["message"]))
            socketUDP = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
            address= arp_table_address_droni[packet["destinationIP"]]
            socketUDP.sendto(json.dumps(newPacket).encode('utf8'), address)
            socketUDP.close()
        else:
            newPacket["destinationIP"] = packet["sourceIP"]
            newPacket["message"] = "errore, ip non trovato"
            sendTCP(newPacket)
    except Exception as err:
        print("send UDP - " + str(err))        

def reciveTCP():
    try:
        while True:
            data = connectionSocket.recv(buffer)
            packet = json.loads(data.decode())
            message =  packet["message"];
            elapsedTime = time.time() - packet["time"]
            print("\n\trecive from CLIENT:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"]))       
            if message == "IP address request":
                packet["message"]="IP assegnato"
                packet["destinationIP"]=ClientIP
                sendTCP(packet)
            else :
                sendUDP(packet)
    except: 
        print("\nGateway -> close socket TCP")
           
def sendTCP(packet):
    global ClientMac
    newPacket = {
            "sourceMAC":myMAC,
            "destinationMAC":ClientMac,
            "sourceIP":interfaceClientIP,
            "destinationIP":packet["destinationIP"],
            "message":packet["message"],
            "time":time.time()
        }
    try:
        connectionSocket.send(json.dumps(newPacket).encode('utf8'))
        print("\n\tsend to CLIENT:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(newPacket["sourceIP"], newPacket["sourceMAC"], newPacket["destinationIP"], newPacket["destinationMAC"], newPacket["message"]))
    except:
        print("\nClient turned off")


#socketClient
socketInterfaceClient = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
socketInterfaceClient.bind(("localhost",int(interfaceClientPort)))
socketInterfaceClient.listen(1)
print ('Waiting for client...') 
#Thread droni in anscolto

def close():
    print( '\n\nClose gateway.')
    try:
        socketInterfaceClient.close()
        connectionSocket.close()
        socketUDP.close()
    finally:
      sys.exit(0)

#definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
    close()

#interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
signal.signal(signal.SIGINT, signal_handler)

threadUDP = threading.Thread(target=reciveUDP, args=())
threadTCP= threading.Thread(target=reciveTCP, args=())

#Stabilisce la connessione, ossia sul socket si prepara ad accettare connessioni in entrata all'indirizzo e porta definiti
  ##### bloccante nel caso il Client non si connette i droni non si connettono
try:
    threadUDP.start()
    connectionSocket, addr = socketInterfaceClient.accept()
    threadTCP.start() 
except IOError as err:
    print ("Error thread - " + str(err)) 
    connectionSocket.close()
print("\nStart connections...  (Exit: Ctrl+C)")
#aspetta la chiusura del client TCP  
threadTCP.join()
input("enter to close")
close()

