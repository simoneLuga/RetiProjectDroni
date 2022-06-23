#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:51:53 2022

@author: simonelugaresi
"""
from socket import * #importiamo la <class 'type'> invece dell'intero modulo

serverPort=84
serverSocket = socket(AF_INET, SOCK_STREAM)
# associa il socket alla porta scelta
serverSocket.bind(('',serverPort))
serverSocket.listen(1)


print ('the web server is up on port:',serverPort)

while True:
    print ('Ready to serve...')
    #Stabilisce la connessione, ossia sul socket si prepara ad accettare connessioni in entrata all'indirizzo e porta definiti
    connectionSocket, addr = serverSocket.accept()
    try:
        while True:
            message = connectionSocket.recv(1024) ## riceve il messaggio di richiesta dal clien
            print(message)
            while True:
                sleep(10)
                connectionSocket.send("TEST".encode())    
    except IOError:
 #Invia messaggio di risposta per file non trovato
        connectionSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n","UTF-8"))
        connectionSocket.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n","UTF-8"))
        connectionSocket.close()
serverSocket.close()
connectionSocket.close()
sys.exit() ## Termina il programma dopo aver inviato i dati corrispondenti
