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

myIP = "10.10.10.1"
myMAC = "00:00:00:00"

interfaceClientIP = "10.10.10.1/24"
interfaceClientPort = "80"
interfaceClientMac = "undefined"

interfaceDroneIP = "192.168.1.1/24"
interfaceDronePort = "81"
interfaceDroneMac = "undefined"

ClientIP = ""
ClientMac = ""
#inizilize sock
sock = socket(AF_INET, SOCK_DGRAM)

def udpRequest():
    global sock
    sock = socket(AF_INET, SOCK_DGRAM)
    server_address = ('localhost', int(interfaceDronePort))
    sock.bind(server_address)
    while True:
        data, address = sock.recvfrom(buffer)
        packet = json.loads(data.decode('utf8'))
        if packet["message"]== "close":
            break        
        if packet["message"] == "disponibile":
            arp_table_address_droni[packet["sourceIP"]] = address
            arp_table_mac_droni[packet["sourceIP"]] = packet["sourceMAC"]
            sendMessage(packet["sourceIP"] + " disponibile")
        #log     
        print("log\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))

    
def sendUDP(ip,indirizzo):
    packet = {
            "sourceMAC":myMAC,
            "destinationMAC":arp_table_mac_droni[ip],
            "sourceIP":myIP,
            "destinationIP":ip,
            "message":indirizzo
        }
    
    sock = socket(AF_INET, SOCK_DGRAM)
    address = arp_table_address_droni[ip]
    sock.sendto(json.dumps(packet).encode('utf8'), address)
    sock.close()
    del arp_table_address_droni[ip]
    #del arp_table_mac_droni[ip]

def listDisponibili():
    return "Sono disponibili i seguenti droni:\n"+str(arp_table_address_droni.keys())
    

def reciveMessage():
    while True:
        packet = json.loads(connectionSocket.recv(buffer).decode())
        message =  packet["message"];
        #log
        print("log\nmittente -> {0} | {1} \nricevente -> {2} | {3} \nmessage: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
        
        #mi salvo IP e mac Specifico del Client
        global ClientIP, ClientMac
        ClientIP = packet["sourceIP"]
        ClientMac = packet["sourceMAC"]
        
        if message =="CLOSE": 
            break
        elif message =="LIST" :
            sendMessage(listDisponibili())
        else :
            if packet["destinationIP"] in arp_table_address_droni.keys():
                sendUDP(packet["destinationIP"], message)
                sendMessage("{} partito".format(packet["destinationIP"]))
            else:
                sendMessage("{} non disponibile".format(packet["destinationIP"]))
    
    print("Gateway : close socket from client")
    socketInterfaceClient.close()
    connectionSocket.close()
    global sock
    sock.close()
    sys.exit(0) 
    
def sendMessage(message):
    global ClientIP, ClientMac
    packet = {
            "sourceMAC":myMAC,
            "destinationMAC":ClientMac,
            "sourceIP":myIP,
            "destinationIP": ClientIP,
            "message":message
        }
    try:
        connectionSocket.send(json.dumps(packet).encode('utf8'))
    except:
        print("Server close")
        
#Thread droni in anscolto
thread3 = threading.Thread(target=udpRequest, args=())
thread3.start()


socketInterfaceClient = socket(AF_INET, SOCK_STREAM)
socketInterfaceClient.bind(("localhost",int(interfaceClientPort)))
socketInterfaceClient.listen(1)

print ('Start client comunication...')
#Stabilisce la connessione, ossia sul socket si prepara ad accettare connessioni in entrata all'indirizzo e porta definiti
connectionSocket, addr = socketInterfaceClient.accept()  ##### bloccante nel caso il Client non si connette i droni non si connettono
try:
    thread1 = threading.Thread(target=reciveMessage, args=())
    thread1.start()
except IOError:
    connectionSocket.close()

