''' Esercitazione 5 - Corso di Programmazione di Reti - Universit�  di Bologna'''

#!/bin/env python
import sys, signal
import http.server
import socketserver
import time
import threading
import socket as sk





class TestHandler (socketserver.BaseRequestHandler):
    
    def handle(self):
        data = self.request[0].strip()
        print("data : "+data.decode())
        print("Sono TCP handler")   
        print(tempVar)
        testSend(self.client_address)
        server.shutdown()
        server.server_close()


def testSend(addr):
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    sock.sendto("sisisisi".encode(), addr)
    
# Legge il numero della porta dalla riga di comando
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8096

tempVar = "priovaa"
# Nota ForkingTCPServer non funziona su Windows come os.fork ()
# La funzione non è disponibile su quel sistema operativo. Invece dobbiamo usare il
# ThreadingTCPServer per gestire più richieste
server = socketserver.ThreadingUDPServer(('',port), TestHandler )
print ("sono andato avanti")

#Assicura che da tastiera usando la combinazione
#di tasti Ctrl-C termini in modo pulito tutti i thread generati
server.daemon_threads = True  
#il Server acconsente al riutilizzo del socket anche se ancora non è stato
#rilasciato quello precedente, andandolo a sovrascrivere
server.allow_reuse_address = True  

#definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if( server ):
        server.server_close()
    finally:
      sys.exit(0)

#interrompe l’esecuzione se da tastiera arriva la sequenza (CTRL + C) 
signal.signal(signal.SIGINT, signal_handler)

threading.Thread(target=server.serve_forever).start()

"""
# entra nel loop infinito
try:
  while True:
    #sys.stdout.flush()
    print("si")
    server.serve_forever()
    print("ok")
except KeyboardInterrupt:
    
  pass

server.server_close()"""
