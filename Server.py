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
	KundenNameList.insert(x, "x")
	KundenAdrList.insert(x, "x")
	KundenTelList.insert(x, "x")
	KundenNotizList.insert(x, "x")

# LOAD
print("LOAD Database Stock")
for eachDir in os.listdir("Stock/"):
	for eachFile in os.listdir("Stock/" + eachDir):
		datei = "Stock/" + eachDir + "/" + eachFile
		eachFile = int(eachFile)
		StockArtikelList.insert(eachFile, BlueLoad("Artikel", datei))
		StockNameList.insert(eachFile, BlueLoad("Name", datei))
		StockOrtList.insert(eachFile, BlueLoad("Ort", datei))
		StockPreisEKList.insert(eachFile, BlueLoad("PreisEK", datei))
		StockPreisVKHList.insert(eachFile, BlueLoad("PreisVKH", datei))
		StockPreisVKList.insert(eachFile, BlueLoad("PreisVK", datei))
		StockAnzahlList.insert(eachFile, BlueLoad("Anzahl", datei))

print("LOAD Database Kunden")
for eachDir in os.listdir("Kunden/"):
	for eachFile in os.listdir("Kunden/" + eachDir):
		datei = "Kunden/" + eachDir + "/" + eachFile
		eachFile = int(eachFile)
		KundenNameList.insert(eachFile, BlueLoad("Name", datei))
		KundenAdrList.insert(eachFile, BlueLoad("Adr", datei))
		KundenTelList.insert(eachFile, BlueLoad("Tel", datei))
		KundenNotizList.insert(eachFile, BlueLoad("Notiz", datei))

# Ordner
BlueMkDir("Arbeitskarten")
for x in range(0, 10):	BlueMkDir("Arbeitskarten/" + str(x))
BlueMkDir("Kunden")
for x in range(0, 10):	BlueMkDir("Kunden/" + str(x))
BlueMkDir("Rechnungen")
for x in range(0, 10):	BlueMkDir("Rechnungen/" + str(x))
BlueMkDir("Stock")


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
		Debug("Data : " + data)

		mode = data.split("(zKz)")[0]; Debug("Mode : " + mode)

		Antwort = ""

		if mode == "GetKunde":
			IDSuche = int(data.split("(zKz)")[1])
			Debug("ID : " + IDSuche)
		
			Antwort = str(KundenNameList[IDSuche]) + "&KK&" + str(KundenTelList[IDSuche]) + "&KK&" + str(KundenAdrList[IDSuche]) + "&KK&" + str(KundenNotizList[IDSuche])

		if mode == "AddKunde":
			NameSuche = data.split("(zKz)")[1].split("(zkz)")[0]
			Debug("Name : " + NameSuche)
			TelSuche = data.split("(zKz)")[1].split("(zkz)")[1]
			Debug("Tel : " + TelSuche)
			AdrSuche = data.split("(zKz)")[1].split("(zkz)")[2]
			Debug("Adr : " + AdrSuche)
			
			KundeID = 0
			while True:
				Debug("KundeID : " + str(KundeID))
				if KundenNameList[KundeID] == "x": break
				else: KundeID = KundeID + 1
			
			KundenNameList[KundeID] = NameSuche
			KundenTelList[KundeID] = TelSuche
			KundenAdrList[KundeID] = AdrSuche
			datei = "Kunden/" + str(KundeID)[-1] + "/" + str(KundeID)
			BlueSave("Name", NameSuche, datei)
			BlueSave("Tel", TelSuche, datei)
			BlueSave("Adr", AdrSuche, datei)
		
			Antwort = str(KundeID)


		if mode == "SearchKunden":
			IDSuche = data.split("(zKz)")[1].split("(zkz)")[0]
			Debug("ID : " + IDSuche)
			NameSuche = data.split("(zKz)")[1].split("(zkz)")[1]
			Debug("Name : " + NameSuche)
			TelSuche = data.split("(zKz)")[1].split("(zkz)")[2]
			Debug("Tel : " + TelSuche)
			AdrSuche = data.split("(zKz)")[1].split("(zkz)")[3]
			Debug("Adr : " + AdrSuche)
			
			for eachKunde in range(0, 1000):
				NameKunde = KundenNameList[eachKunde]
				TelKunde = KundenTelList[eachKunde]
				AdrKunde = KundenAdrList[eachKunde]
				Gefunden = True
				if not NameKunde == "x":
					#	ID
					if not IDSuche in str(eachKunde): Gefunden = False
					#	Name
					for TeilNameSuche in NameSuche.split(" "):
						if not TeilNameSuche.lower() in NameKunde.lower(): Gefunden = False
					#	Tel
					TelGefunden = False
					for TeilTelSuche in TelSuche.split(" "):
						if TeilTelSuche in TelKunde:
							TelGefunden = True
					if not TelGefunden: Gefunden = False
					#	Adr
					for TeilAdrSuche in AdrSuche.split(" "):
						if not TeilAdrSuche.lower() in AdrKunde.lower(): Gefunden = False
					if Gefunden:
						if Antwort == "": Antwort = str(eachKunde) + "&KK&" + str(NameKunde) + "&KK&" + str(TelKunde) + "&KK&" + str(AdrKunde)
						else: Antwort = Antwort + "&K()K&" + str(eachKunde) + "&KK&" + str(NameKunde) + "&KK&" + str(TelKunde) + "&KK&" + str(AdrKunde)

		Debug("Sende : " + str(Antwort))
		Antwort = Antwort.encode()
		c.send(Antwort)
c.close()
