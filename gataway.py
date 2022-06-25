#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:40:12 2022

@author: simonelugaresi
"""
from socket import *
from handlerUDP import Handler
import socketserver
import json
import time
import threading
import sys

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

packet=""

"""
packet = {
        "sourceMAC":"",
        "destinationMAC":"",
        "sourceIP":"",
        "destinationIP":"",
        "message":""
    }"""

arp_table_address_droni = {}
arp_table_mac_droni = {}

interfaceClientIP = "10.10.10.1/24"
interfaceClientPort = "8062"
interfaceClientMac = "undefined"

interfaceDroneIP = "102.168.1.1/24"
interfaceDronePort = "8063"
interfaceDroneMac = "undefined"

def udpRequest():
    sock = socket(AF_INET, SOCK_DGRAM)
    server_address = ('localhost', int(interfaceDronePort))
    sock.bind(server_address)
    ok = True
    while ok:
        data, address = sock.recvfrom(4096)
        #print ("IP: "+str(address[0])+" - port: "+str(address[1])+"  - message: "+data.decode('utf8'))
        #global packet
        packet = json.loads(data.decode('utf8'))
        #sent = sock.sendto(data, address)
        if packet["message"]== "close": ok = False
        
        if packet["message"] == "disponibile":
            arp_table_address_droni[packet["sourceIP"]] = address
            arp_table_mac_droni[packet["sourceIP"]] = packet["sourceMAC"]
            sendMessage(packet["sourceIP"] + " disponibile")
            
        print("{0} | {1} | {2} | {3} | message: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
        
        
        #socketInterfaceDrone = socketserver.UDPServer(("localhost", 8085), Handler )
        #request  = socketInterfaceDrone.get_request()
        #data = request[0]
        #socket = request[1]
        #print(data)
    
def sendUDP(ip,indirizzo):
    packet = {
            "sourceMAC":"undefined",
            "destinationMAC":arp_table_mac_droni[ip],
            "sourceIP":"undefined",
            "destinationIP":ip,
            "message":indirizzo
        }
    
    sock = socket(AF_INET, SOCK_DGRAM)
    address = arp_table_address_droni[ip]
    sock.sendto(json.dumps(packet).encode('utf8'), address)
    del arp_table_address_droni[ip]
    #del arp_table_mac_droni[ip]
    
    


def reciveMessage():
    packet = json.loads(connectionSocket.recv(1024).decode())
    message =  packet["message"];
    print("{0} | {1} | {2} | {3} | message: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
    while message!="close":
        if packet["destinationIP"] in arp_table_address_droni.keys():
            sendUDP(packet["destinationIP"], message)
            sendMessage("{} partito".format(packet["destinationIP"]))
        else:
            sendMessage("{} non disponibile".format(packet["destinationIP"]))
       
        packet = json.loads(connectionSocket.recv(1024).decode())
        message =  packet["message"];
        print("{0} | {1} | {2} | {3} | message: {4}".format(packet["sourceIP"], packet["sourceMAC"], packet["destinationIP"], packet["destinationMAC"], packet["message"]))
       
        
    print("Gateway : close socket")
    socketInterfaceClient.close()
    connectionSocket.close()
    #socketInterfaceDrone.shutdown()
    sys.exit(0) 
    
def sendMessage(message):
    packet = {
            "sourceMAC":"undefined",
            "destinationMAC":"undefinded",
            "sourceIP":"undefined",
            "destinationIP":"undefined",
            "message":message
        }
    
    try:
        connectionSocket.send(json.dumps(packet).encode('utf8'))
    except:
        print("Server close")
        





###socketInterfaceDrone = socketserver.ThreadingUDPServer(("localhost", int(interfaceDronePort)), Handler )
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
   # thread2 = threading.Thread(target=sendMessage, args=())
    #thread2.start()
        
        
except IOError:
    #Invia messaggio di risposta per file non trovato

    connectionSocket.close()



# entra nel loop infinito
"""
try:
  while True:
    #sys.stdout.flush()
    socketInterfaceDrone.serve_forever()
except KeyboardInterrupt:
    
  pass"""
"""
server_thread = threading.Thread(target=socketInterfaceDrone.serve_forever)
# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
print("Server loop running in thread:", server_thread.name)

print("OKOK")"""

##socketInterfaceDrone.serve_forever()

#socketInterfaceDrone.server_close()



    
    
    
    
"""
class Gataway:
    
    def __init__(self, interfaceClientIP, interfaceClientPort, interfeaceDroneIP, interfaceDronePort):
        self.interfaceClientIP = interfaceClientIP
        self.interfaceClientPort = interfaceClientPort
        self.interfaceDronePort = interfaceDronePort
        self.interfeaceDroneIP = interfeaceDroneIP
        self.socketForClient = socket(AF_INET,SOCK_STREAM) #Indirizzi IPv4 e socket TCP
        self.secketForClient.bind(('', portClient))
        self.socketForClient.listen(1)#in quanto dovremmo utilizzare una sola connessione alla volta con il client
        #TODO intefaccia UDP per Drone
    
    
    def listenClient(self):
        while True:
            print("Ready for Client connection")
            connectionSocket, addr = self.socketForClient.accept()
            try:
                message = connectionSocket.recv(1024) #TODO: decidere dimensioni buffer# riceve il messaggio di richiesta dal client
                print(message)
                
            except IOError:
         #Invia messaggio di risposta per file non trovato
                connectionSocket.send(bytes("404 Not Found","UTF-8"))
                connectionSocket.close()    


x = Gataway("", 8080, "interfeaceDroneIP", "interfaceDronePort")
x.listenClient()
"""