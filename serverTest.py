#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:29:24 2022

@author: alex
"""


import socketserver


class MyTCP(socketserver.BaseRequestHandler):
    def handle(self):
        print("TCP handler")

#socketUDP = socketserver.ThreadingUDPServer(("localhost", 8085), handlerUDP.Handler )
socketTCP = socketserver.ThreadingTCPServer(("localhost", 8089), MyTCP )

x = input("wait: ")
print("ok")