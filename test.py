
'''Client:

  After you run the server,
  use command line "client.py localhost portnumber index.htm" to run the client.
  
  You can not run the client by IDLE(Python GUI).
'''

from socket import *
import time
import threading
import sys

    
clientsocket = socket(AF_INET, SOCK_STREAM)

request = "CIAO"
try:
    clientsocket.connect(('',84))
except Exception as data:
    print (Exception,":",data)
    print ("Please try again.\r\n")
    sys.exit(0)

request = input("Client vuole dire:")
clientsocket.send(request.encode())

def ricezione(clientsocket):
    while True:
        response = clientsocket.recv(1024)
        print(response)

thread = threading.Thread(target=ricezione, args=(clientsocket))
thread.start()


    

   
   
   
   
   
   
   
   
   
   