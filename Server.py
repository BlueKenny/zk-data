#!/usr/bin/env python3.6
import sys
import socket
from debug import *

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
