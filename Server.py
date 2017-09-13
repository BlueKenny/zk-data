#!/usr/bin/env python3
import sys
import socket
from debug import *
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
import os
import datetime
now = datetime.datetime.now()

if not os.path.exists("DATA"): BlueSave("KundenMAX", 0, "DATA")
KundenMAX = int(BlueLoad("KundenMAX", "DATA"))
Debug("KundenMAX : " + str(KundenMAX))


# Ordner
BlueMkDir("Arbeitskarten")
for x in range(0, 10):	BlueMkDir("Arbeitskarten/" + str(x))
BlueMkDir("Kunden")
for x in range(0, 10):	BlueMkDir("Kunden/" + str(x))
BlueMkDir("Rechnungen")
for x in range(0, 10):	BlueMkDir("Rechnungen/" + str(x))
BlueMkDir("Stock")
BlueMkDir("StockBewegung")

StockBarcodeList = []
StockArtikelList = []
StockLieferantList = []
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
for x in range(100000, 999999):
	StockBarcodeList.insert(x, "x")
	StockArtikelList.insert(x, "x")
	StockLieferantList.insert(x, "x")
	StockNameList.insert(x, "x")
	StockOrtList.insert(x, "x")
	StockPreisEKList.insert(x, "x")
	StockPreisVKHList.insert(x, "x")
	StockPreisVKList.insert(x, "x")
	StockAnzahlList.insert(x, "x")
for x in range(0, KundenMAX):
	KundenNameList.insert(x, "x")
	KundenAdrList.insert(x, "x")
	KundenTelList.insert(x, "x")
	KundenNotizList.insert(x, "x")

# LOAD
print("LOAD Database Stock")
StockArtikelAnzahl = 0
for eachDir in os.listdir("Stock/"):
	for eachFile in os.listdir("Stock/" + eachDir):
		datei = "Stock/" + eachDir + "/" + eachFile
		eachFile = int(eachFile)
		StockBarcodeList[eachFile]=BlueLoad("Barcode", datei)
		StockArtikelList[eachFile]=BlueLoad("Artikel", datei)
		StockLieferantList[eachFile]=BlueLoad("Lieferant", datei)
		StockNameList[eachFile]=BlueLoad("Name", datei)
		StockOrtList[eachFile]=BlueLoad("Ort", datei)
		StockPreisEKList[eachFile]=BlueLoad("PreisEK", datei)
		StockPreisVKHList[eachFile]=BlueLoad("PreisVKH", datei)
		StockPreisVKList[eachFile]=BlueLoad("PreisVK", datei)
		StockAnzahlList[eachFile]=BlueLoad("Anzahl", datei)
		StockArtikelAnzahl  = StockArtikelAnzahl  + 1
print(StockArtikelAnzahl)

print("LOAD Database Kunden")
for eachFile in range(0, KundenMAX + 1):
		datei = "Kunden/" + str(eachFile)[-1] + "/" + str(eachFile)
		if os.path.exists(datei):
			eachFile = int(eachFile)
			KundenNameList[eachFile]=BlueLoad("Name", datei)
			KundenAdrList[eachFile]=BlueLoad("Adr", datei)
			KundenTelList[eachFile]=BlueLoad("Tel", datei)
			KundenNotizList[eachFile]=BlueLoad("Notiz", datei)
		else: Debug("Kunde " + str(eachFile) + " nicht gefunden")

SERVER_IP = ("", 10000)
s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(SERVER_IP)
s.listen(1)

def Date():
	return now.strftime("%Y-%m-%d")

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

		Antwort = "x"

		if mode == "SaveKunde":
			ID = data.split("(zKz)")[1].split("(zkz)")[0]
			Name = data.split("(zKz)")[1].split("(zkz)")[1]
			Tel = data.split("(zKz)")[1].split("(zkz)")[2]
			Adr = data.split("(zKz)")[1].split("(zkz)")[3]
			Notiz = data.split("(zKz)")[1].split("(zkz)")[4]
			datei = "Kunden/" + str(ID)[-1] + "/" + str(ID)
			KundenNameList[int(ID)] = Name
			KundenTelList[int(ID)] = Tel
			KundenAdrList[int(ID)] = Adr
			KundenNotizList[int(ID)] = Notiz
			BlueSave("Name", Name, datei)
			BlueSave("Tel", Tel, datei)
			BlueSave("Adr", Adr, datei)
			BlueSave("Notiz", Notiz, datei)
			Antwort = "SaveKundeOK"

		if mode == "GetArbeitskartenVonKunde":
			Debug("")
			

		if mode == "GetKunde":
			IDSuche = int(data.split("(zKz)")[1])
			Debug("ID : " + str(IDSuche))
		
			Antwort = str(KundenNameList[IDSuche]) + "&KK&" + str(KundenTelList[IDSuche]) + "&KK&" + str(KundenAdrList[IDSuche]) + "&KK&" + str(KundenNotizList[IDSuche])
		
		if mode == "StockSetArtInfo":
			ID = int(data.split("(zKz)")[1].split("(zkz)")[0])
			VarName = str(data.split("(zKz)")[1].split("(zkz)")[1])
			Var = str(data.split("(zKz)")[1].split("(zkz)")[2])
			Debug("ID :  " + str(ID))
			Debug("VarName :  " + str(VarName))
			Debug("Var :  " + str(Var))
			BlueMkDir("Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1])

			if VarName == "Barcode": 
				StockBarcodeList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), "Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Artikel": 
				StockArtikelList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), "Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Lieferant": 
				StockLieferantList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), "Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Name":  
				StockNameList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), "Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Ort":  
				StockOrtList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), "Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "PreisEK":  
				StockPreisEKList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), "Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "PreisVKH":  
				StockPreisVKHList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), "Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "PreisVK":  
				StockPreisVKList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), "Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Anzahl":  
				StockAnzahlList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), "Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))

		if mode == "StockGetArtInfo":
			ID = int(data.split("(zKz)")[1].split("(zkz)")[0])
			Var = str(data.split("(zKz)")[1].split("(zkz)")[1])
			Debug("ID :  " + str(ID))
			Debug("Var :  " + str(Var))

			try:
				if Var == "Artikel":  Antwort = str(StockArtikelList[ID])
				if Var == "Name":  Antwort = str(StockNameList[ID])
				if Var == "Ort":  Antwort = str(StockOrtList[ID])
				if Var == "PreisEK":  Antwort = str(StockPreisEKList[ID])
				if Var == "PreisVKH":  Antwort = str(StockPreisVKHList[ID])
				if Var == "PreisVK":  Antwort = str(StockPreisVKList[ID])
				if Var == "Anzahl":  Antwort = str(StockAnzahlList[ID])
				if Var == "Barcode":  Antwort = str(StockBarcodeList[ID])
				if Var == "Lieferant":  Antwort = str(StockLieferantList[ID])
			except:
				Antwort = "None"
			if Antwort == "": Antwort = "None"

		if mode == "GetStockZahl":
			Antwort = str(StockArtikelAnzahl)

		if mode == "ChangeStock":
			BcodeSuche = int(data.split("(zKz)")[1].split("(zkz)")[0])
			Debug("BcodeSuche : " + str(BcodeSuche))
			NewStock = data.split("(zKz)")[1].split("(zkz)")[1]
			Debug("NewStock : " + NewStock)
			AltStock = str(StockAnzahlList[BcodeSuche])
			Debug("AltStock : " + AltStock )
			StockAnzahlList[BcodeSuche] = int(AltStock) + int(NewStock)
			BlueSave("Anzahl", StockAnzahlList[BcodeSuche], "Stock/" + str(BcodeSuche)[-3] + str(BcodeSuche)[-2] + str(BcodeSuche)[-1] + "/" + str(BcodeSuche))
			open( "StockBewegung/" + str(Date()), "a").write("\n" + str(BcodeSuche) + " from " + str(AltStock) + " to " + str(StockAnzahlList[BcodeSuche]))

		if mode == "SearchStock":
			BcodeSuche = data.split("(zKz)")[1].split("(zkz)")[0]
			Debug("BcodeSuche : " + BcodeSuche)
			BarcodeSuche = data.split("(zKz)")[1].split("(zkz)")[1]
			Debug("BarcodeSuche : " + BarcodeSuche)
			ArtikelSuche = data.split("(zKz)")[1].split("(zkz)")[2]
			Debug("ArtikelSuche : " + ArtikelSuche)
			OrtSuche = data.split("(zKz)")[1].split("(zkz)")[3]
			Debug("OrtSuche : " + OrtSuche)
			
			if not BcodeSuche.rstrip() == "":
				Debug("BcodeSuche")
				try:
					indices = [BcodeSuche]
					Debug("BcodeSuche YES")
				except: indices[0]
			else:
				Debug("BarcodeSuche")
				if not BarcodeSuche.rstrip() == "":
					try: indices = [StockBarcodeList.index(BarcodeSuche)]
					except: indices = [0]
				else:
					Debug("ArtikelSuche")
					if not ArtikelSuche == "":
						indices = [i for i, x in enumerate(StockArtikelList) if ArtikelSuche in x]
						indices = indices[:20]
					else:
						Debug("OrtSuche")
						if not OrtSuche == "":
							indices = [i for i, x in enumerate(StockOrtList) if OrtSuche in x]
						else: indices = [0]
			try:
				Debug("indices : " + str(indices))
				Antwort = " "
				for eachDat in indices:
					Debug("eachDat : " + str(eachDat))
					eachDat = int(eachDat)
					Antwort = Antwort + str(eachDat) + " | " + str(StockArtikelList[eachDat]) + " | " + str(StockLieferantList[eachDat]) + " | " + str(StockNameList[eachDat]) + " | " + str(StockOrtList[eachDat]) + " | " + str(StockPreisEKList[eachDat]) + " | " + str(StockPreisVKHList[eachDat]) + " | "+ str(StockPreisVKList[eachDat]) + " | " + str(StockAnzahlList[eachDat]) + "<K>"

			except: Debug("Nichts gefunden")

		if mode == "AddKunde":
			NameSuche = data.split("(zKz)")[1].split("(zkz)")[0]
			Debug("Name : " + NameSuche)
			TelSuche = data.split("(zKz)")[1].split("(zkz)")[1]
			Debug("Tel : " + TelSuche)
			AdrSuche = data.split("(zKz)")[1].split("(zkz)")[2]
			Debug("Adr : " + AdrSuche)
			
			KundenMAX = KundenMAX + 1
			KundeID = KundenMAX

			KundenNameList.insert(KundeID, NameSuche)
			KundenTelList.insert(KundeID, TelSuche)
			KundenAdrList.insert(KundeID, AdrSuche)
			datei = "Kunden/" + str(KundeID)[-1] + "/" + str(KundeID)
			BlueSave("Name", NameSuche, datei)
			BlueSave("Tel", TelSuche, datei)
			BlueSave("Adr", AdrSuche, datei)
		
			BlueSave("KundenMAX", KundenMAX, "DATA")
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
			
			while True:
				#	ID
				if not IDSuche == "":
					if int(IDSuche) > int(KundenMAX): break
					Debug("Suche mit ID " + str(IDSuche))
					IDSuche = int(IDSuche)
					NameKunde = KundenNameList[IDSuche]
					TelKunde = KundenTelList[IDSuche]
					AdrKunde = KundenAdrList[IDSuche]
					Antwort = str(IDSuche) + "&KK&" + str(NameKunde) + "&KK&" + str(TelKunde) + "&KK&" + str(AdrKunde)
					break

				
			#for eachKunde in range(0, 1000):
				#NameKunde = KundenNameList[eachKunde]
				#TelKunde = KundenTelList[eachKunde]
				#AdrKunde = KundenAdrList[eachKunde]
				#Gefunden = True
				#if not NameKunde == "x":
					
					#	Name
				#	for TeilNameSuche in NameSuche.split(" "):
				#		if not TeilNameSuche.lower() in NameKunde.lower(): Gefunden = False
					#	Tel
				#	TelGefunden = False
				#	for TeilTelSuche in TelSuche.split(" "):
				#		if TeilTelSuche in TelKunde:
				#			TelGefunden = True
				#	if not TelGefunden: Gefunden = False
					#	Adr
				#	for TeilAdrSuche in AdrSuche.split(" "):
				#		if not TeilAdrSuche.lower() in AdrKunde.lower(): Gefunden = False
				#	if Gefunden:
				#		if Antwort == "": Antwort = str(eachKunde) + "&KK&" + str(NameKunde) + "&KK&" + str(TelKunde) + "&KK&" + str(AdrKunde)
				#		else: Antwort = Antwort + "&K()K&" + str(eachKunde) + "&KK&" + str(NameKunde) + "&KK&" + str(TelKunde) + "&KK&" + str(AdrKunde)

		Debug("Sende : " + str(Antwort))
		Antwort = Antwort.encode()
		c.send(Antwort)
c.close()
