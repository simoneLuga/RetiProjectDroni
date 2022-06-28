#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:40:12 2022

@author: Alex e Simone
"""
import socket as sk
import json
import threading
import sys
import ipaddress as ipaddr
import time

packet=""

buffer = 1024

myMAC = "00:00:00:00"

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
ClientMac = "00:00:00:11"

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
    
    if ip not in arp_table_address_droni.keys():
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

def availableDrones():
    temp = "Droni disponibili -> "
    for val in arp_table_address_droni.keys():
       temp +=str(val)+" - "
    return temp
    
def closeAll():
    tempList = arp_table_address_droni.copy()
    for ip in tempList.keys():
        sendUDP(ip, "CLOSE")
    socketInterfaceClient.close()
    connectionSocket.close()
         
def reciveUDP():
    global socketUDP
    socketUDP = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    server_address = ('localhost', int(interfaceDronePort))
    socketUDP.bind(server_address)
    while True:
        try:
            data, address = socketUDP.recvfrom(buffer)
            packet = json.loads(data.decode('utf8'))   
            elapsedTime = time.time() - packet["time"]
            print("\n\trecive from DRONE:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"]))       
            if packet["message"] == "IP address request":
                assignmentIP(packet["sourceMAC"], address)  
            else:
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
    newPacket["destinationMAC"] = "XXX"
    try:
        if packet["destinationIP"] == broadcast:
            print("\n\tsend to DRONE:\nSender: {0} | {1} -> Receiver: {2} | {3} \nmessage: {4}".format(newPacket["sourceIP"], newPacket["sourceMAC"], newPacket["destinationIP"], newPacket["destinationMAC"], newPacket["message"]))
            print(str(arp_table_address_droni))
            print(str(arp_table_mac_droni))
            for address in arp_table_address_droni.values():
                    socketUDP = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
                    socketUDP.sendto(json.dumps(newPacket).encode('utf8'), address)
                    print("ho inviato")
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
    while True:
        try:
            data = connectionSocket.recv(buffer)
            packet = json.loads(data.decode())
            message =  packet["message"];
            elapsedTime = time.time() - packet["time"]
            print("\n\trecive from CLIENT:\nSender: {0} | {1} -> receiver: {2} | {3} \nTime elapsed: {4}\nPacket size: {5} byte\nmessage: {6}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], elapsedTime,str(sys.getsizeof(data)),packet["message"]))       
            if message == "IP address request":
                packet["message"]="IP assegnato"
                sendTCP(packet)
            else :
                sendUDP(packet)
        except Exception as err: 
           print("recive TCP - " + str(err))  
           
    print("\nGateway -> close socket TCP")
    # TODO closeAll()
    
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
print("\nStart connections...")
#aspetta la chiusura del client TCP  
threadTCP.join()
socketUDP.close()
threadUDP.join()
print("by =)")
sys.exit(0)

