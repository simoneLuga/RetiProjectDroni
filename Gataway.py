#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:40:12 2022

@author: simonelugaresi
"""
from socket import *
import json

def JSonToData(message):
    data = json.load(message)
    drone = data.drone
    Indirizzo = data.Indirizzo

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
