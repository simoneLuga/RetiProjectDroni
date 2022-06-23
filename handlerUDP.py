#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 17:22:34 2022

@author: alex
"""
import socketserver
import time

class Handler (socketserver.BaseRequestHandler):
    
    def handle(self):
        print("start handler")
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print("sono l handler: "+data)
        #socket.sendto(data.upper(), self.client_address)