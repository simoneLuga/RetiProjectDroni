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

def JSonToData(message):
    data = json.load(message)
    drone = data.drone
    Indirizzo = data.Indirizzo

def reciveMessage():
    message = connectionSocket.recv(1024)
    message=  message.decode();
    while message!="close":
        message = connectionSocket.recv(1024)
        message=  message.decode()
        print(message)
        
    print("Gateway : close socket")
    socketInterfaceClient.close()
    connectionSocket.close()
    socketInterfaceDrone.shutdown()
    sys.exit(0) 
    
def sendMessage():
    try:
        while True:
            connectionSocket.send("Sono il gateway ".encode())
            time.sleep(5)
    except:
        print("Server close")
        

interfaceClientIP = "10.10.10.1/24"
interfaceClientPort = "8083"
interfaceClientMac = "undefined"

interfaceDroneIP = "102.168.1.1/24"
interfaceDronePort = "8084"
interfaceDroneMac = "undefined"

socketInterfaceDrone = socketserver.ThreadingUDPServer(("localhost", int(interfaceDronePort)), Handler )

socketInterfaceClient = socket(AF_INET, SOCK_STREAM)
socketInterfaceClient.bind(("localhost",int(interfaceClientPort)))
socketInterfaceClient.listen(1)

print ('Start client comunication...')
#Stabilisce la connessione, ossia sul socket si prepara ad accettare connessioni in entrata all'indirizzo e porta definiti
connectionSocket, addr = socketInterfaceClient.accept()
try:
    thread1 = threading.Thread(target=reciveMessage, args=())
    thread1.start()
    thread2 = threading.Thread(target=sendMessage, args=())
    thread2.start()
        
        
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

socketInterfaceDrone.serve_forever()

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