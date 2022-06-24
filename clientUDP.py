#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 20:42:15 2022

@author: alex
"""

import socket as sk

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
server_address = ('localhost', 8060)

message = input("UDP message: ")
try:

    # inviate il messaggio
    print ('sending "%s"' % message)
    
    sent = sock.sendto(message.encode(), server_address)

    # Ricevete la risposta dal server
    print('waiting to receive from')
    data, server = sock.recvfrom(4096)
    #print(server)
    
    print ('received message "%s"' % data.decode('utf8'))
except Exception as info:
    print(info)
finally:
    print ('closing socket')
    sock.close()