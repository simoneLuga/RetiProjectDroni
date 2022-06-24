#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 10:32:21 2022

@author: alex
"""
import socketserver

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        print("TCP handler")
        
        