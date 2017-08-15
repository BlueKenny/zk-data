#!/usr/bin/env python3.6
import sys
import socket
from debug import *
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
import os
from BlueVar import *
StockArtikelList = []
StockNameList = []
StockOrtList = []
StockPreisEKList = []
StockPreisVKHList = []
StockPreisVKList = []
StockAnzahlList = []
KundenNameList = []
KundenAdrList = []
KundenTelList = []
KundenNotizList = []

Debug("Make Cache")
for x in range(000000, 999999):
	StockArtikelList.insert(x, "x")
	StockNameList.insert(x, "x")
	StockOrtList.insert(x, "x")
	StockPreisEKList.insert(x, "x")
	StockPreisVKHList.insert(x, "x")
	StockPreisVKList.insert(x, "x")
	StockAnzahlList.insert(x, "x")

# LOAD
print("LOAD Database")
for eachDirStock in os.listdir("stock/"):
	for eachFileStock in os.listdir("stock/" + eachDirStock):
		datei = "stock/" + eachDirStock + "/" + eachFileStock
		eachFileStock = int(eachFileStock)
		StockArtikelList.insert(eachFileStock, BlueLoad("Artikel", datei))
		StockNameList.insert(eachFileStock, BlueLoad("Name", datei))
		StockOrtList.insert(eachFileStock, BlueLoad("Ort", datei))
		StockPreisEKList.insert(eachFileStock, BlueLoad("PreisEK", datei))
		StockPreisVKHList.insert(eachFileStock, BlueLoad("PreisVKH", datei))
		StockPreisVKList.insert(eachFileStock, BlueLoad("PreisVK", datei))
		StockAnzahlList.insert(eachFileStock, BlueLoad("Anzahl", datei))

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
