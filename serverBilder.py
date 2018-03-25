#!/usr/bin/env python3
import socket               # Import socket module
import os

if not os.path.exists("Bilder"): os.mkdir("Bilder")

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)
    bild = str(c.recv(1024).decode())
    print("Bild: " + str(bild))
    
    try:
        if os.path.exists("Bilder/" + bild): os.remove("Bilder/" + bild)

        f = open("Bilder/" + bild,'wb')
        print("Receiving...")
        l = c.recv(1024)
        while (l):
            print("Receiving2...")
            f.write(l)
            l = c.recv(1024)
        f.close()
        print("Done Receiving")
        
        #try: ean = os.popen("zbarimg -q " + "get/" + bild).readlines(0)[0].split(":")[1]
        #except: ean = "x"

        #print("ean: " + str(ean))
        
        #c.send(ean.encode())

    
    except: True
    c.close()                # Close the connection
