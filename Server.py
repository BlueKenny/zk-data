#!/usr/bin/env python3.6
import sys
import socket
from debug import *
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave


# Ordner
BlueMkDir("Arbeitskarten")
for x in range(0, 10):	BlueMkDir("Arbeitskarten/" + str(x))
BlueMkDir("Kunden")
for x in range(0, 10):	BlueMkDir("Kunden/" + str(x))
BlueMkDir("Rechnungen")
for x in range(0, 10):	BlueMkDir("Rechnungen/" + str(x))



SERVER_IP = ("", 10000)
s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(SERVER_IP)
s.listen(1)

while True:
	Debug("Warte auf befehl...")
	c, addr = s.accept()
	Debug("Verbunden mit " + str(addr))
	while True:
		data = c.recv(2048)
		if not data:
			Debug("Client sendet nicht mehr")
			break
		data = data.decode()

		Debug(str(data) + " erhalten")

		Antwort = "Suche erfolgreich"






		Antwort = Antwort.encode()
		c.send(Antwort)
c.close()
