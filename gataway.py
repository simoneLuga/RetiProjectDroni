#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:40:12 2022

@author: simonelugaresi
"""
from socket import *
import socketserver
import json
import time
import threading
import sys
import ipaddress as ipaddr
import time

""" Struttura dati del pacchetto
packet = {
        "sourceMAC":"",
        "destinationMAC":"",
        "sourceIP":"",
        "destinationIP":"",
        "message":""
    }"""
packet=""

buffer = 4096

dnsTable = {
    "drone1":"192.168.1.2",
    "drone2":"192.168.1.3",
    "drone3":"192.168.1.4"
}

def dns(nome):
    return dnsTable[nome]

def JSonToData(message):
    data = json.loads(message)
    drone = data.drone
    Indirizzo = data.Indirizzo

arp_table_address_droni = {}
arp_table_mac_droni = {}

networkDroni = "192.168.1.0/24"
networkClient = "10.10.10.0/24"
myMAC = "00:00:00:00"

interfaceClientIP = "10.10.10.1/24"
interfaceClientPort = "8080"
interfaceClientMac = "undefined"

interfaceDroneIP = "192.168.1.1/24"
interfaceDronePort = "8081"
interfaceDroneMac = "undefined"

# IP statico per il client
ClientIP = "10.10.10.2"
ClientMac = "00:00:00:11"

isOn = True


#inizilize sock
sock = socket(AF_INET, SOCK_DGRAM)

def get_ip_from_mac(d, mac):  
    return [k for k, v in d.items() if v == mac]

def assignmentIP(macAddress, address):
    ip = get_ip_from_mac(arp_table_mac_droni, macAddress)
    
    if len(ip)==0:
        for addr in ipaddr.IPv4Network(networkDroni):
        
            if str(addr) not in arp_table_mac_droni.keys() and str(addr)!=(interfaceDroneIP.split("/"))[0] and str(addr)!="192.168.1.0":
                ip =  str(addr)
                arp_table_mac_droni[ip] = macAddress
                break
    else:
        ip = ip[0]
    
    arp_table_address_droni[ip] = address
    sendUDP(ip, "IP assegnato")
    
    

def udpRequest():
    global sock
    sock = socket(AF_INET, SOCK_DGRAM)
    server_address = ('localhost', int(interfaceDronePort))
    sock.bind(server_address)
    
    global isOn
    while isOn:
        data, address = sock.recvfrom(buffer)  #TODO verificare cosa succede quando chiudo sock mentre é in attesa
        packet = json.loads(data.decode('utf8'))
        
        #log     
        print("\nlog recive UDP\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
        
        if packet["message"] == "IP address request":
            assignmentIP(packet["sourceMAC"], address)
            
        elif packet["message"] == "disponibile":
            arp_table_address_droni[packet["sourceIP"]] = address
            arp_table_mac_droni[packet["sourceIP"]] = packet["sourceMAC"]
            sendMessage(packet["sourceIP"] + " disponibile")
        
    
def sendUDP(ip,message):
    packet = {
            "sourceMAC":myMAC,
            "destinationMAC":arp_table_mac_droni[ip],
            "sourceIP":interfaceDroneIP,
            "destinationIP":ip,
            "message": message,
            "time": time.time()
        }
    
    sock = socket(AF_INET, SOCK_DGRAM)
    address = arp_table_address_droni[ip]
    sock.sendto(json.dumps(packet).encode('utf8'), address)
    sock.close()
    del arp_table_address_droni[ip]
    print("\nlog send UDP\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
    #del arp_table_mac_droni[ip]

def listDisponibili():
    return "Sono disponibili i seguenti droni:\n"+str(arp_table_address_droni.keys())
    

def reciveMessage():
    global isOn
    while isOn:
        packet = json.loads(connectionSocket.recv(buffer).decode())
        message =  packet["message"];
        #log
        print("\nlog recive TCP\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
        
        #mi salvo IP e mac Specifico del Client
        #global ClientIP, ClientMac
        #ClientIP = packet["sourceIP"]
        #ClientMac = packet["sourceMAC"]
        
        if message== "IP address request":
            sendMessage("IP assegnato")
        elif message =="CLOSE": 
            isOn = False
        elif message =="LIST" :
            sendMessage(listDisponibili())
        else :
            if packet["destinationIP"] in arp_table_address_droni.keys():
                sendUDP(packet["destinationIP"], message)
                sendMessage("{} partito".format(packet["destinationIP"]))
            else:
                sendMessage("{} non disponibile".format(packet["destinationIP"]))
    
    print("\nGateway : close socket from client")
    socketInterfaceClient.close()
    connectionSocket.close()
    global sock
    sock.close()  #TODO verificare se lo chiudo ma magari non era aperto
    sys.exit(0) 
    
def sendMessage(message):
    global ClientIP, ClientMac
    packet = {
            "sourceMAC":myMAC,
            "destinationMAC":ClientMac,
            "sourceIP":interfaceClientIP,
            "destinationIP": ClientIP,
            "message":message
        }
    try:
        connectionSocket.send(json.dumps(packet).encode('utf8'))
        print("\nlog send TCP\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
    except:
        print("\nServer close")
        
#Thread droni in anscolto
thread3 = threading.Thread(target=udpRequest, args=())
thread3.start()


socketInterfaceClient = socket(AF_INET, SOCK_STREAM)
socketInterfaceClient.bind(("localhost",int(interfaceClientPort)))
socketInterfaceClient.listen(1)

print ('\nStart client comunication...')
#Stabilisce la connessione, ossia sul socket si prepara ad accettare connessioni in entrata all'indirizzo e porta definiti
connectionSocket, addr = socketInterfaceClient.accept()  ##### bloccante nel caso il Client non si connette i droni non si connettono
try:
    thread1 = threading.Thread(target=reciveMessage, args=())
    thread1.start()
except IOError:
    connectionSocket.close()

