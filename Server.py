#!/usr/bin/env python3
import sys
import socket
from debug import *
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
import os
from RoundUp import *
import datetime
now = datetime.datetime.now()

if not os.path.exists("DATA"): BlueSave("KundenMAX", 0, "DATA")
KundenMAX = int(BlueLoad("KundenMAX", "DATA"))
Debug("KundenMAX : " + str(KundenMAX))

# Ordner
BlueMkDir("Stock")
BlueMkDir("StockBewegung")
BlueMkDir("Machinen")

StockBarcodeList = []
StockArtikelList = []
StockLieferantList = []
StockNameList = []
StockOrtList = []
StockPreisEKList = []
StockPreisVKHList = []
StockPreisVKList = []
StockAnzahlList = []
StockMachinenList = []

ListeDerLieferanten = []

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
	StockMachinenList.insert(x, "x")

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
		StockOrtList[eachFile]=str(BlueLoad("Ort", datei)).upper()
		StockPreisEKList[eachFile]=BlueLoad("PreisEK", datei)
		StockPreisVKHList[eachFile]=BlueLoad("PreisVKH", datei)
		StockPreisVKList[eachFile]=BlueLoad("PreisVK", datei)
		StockAnzahlList[eachFile]=BlueLoad("Anzahl", datei)
		StockMachinenList[eachFile]=BlueLoad("Machinen", datei)

		StockArtikelAnzahl  = StockArtikelAnzahl  + 1
		if not StockLieferantList[eachFile] in ListeDerLieferanten: ListeDerLieferanten.append(StockLieferantList[eachFile])
		if not StockMachinenList[eachFile] == None:
			eaThis = "Machinen"
			for ea in range(0, len(str(StockMachinenList[eachFile]).split("/"))):
				eaThis = eaThis + "/" + str(StockMachinenList[eachFile]).split("/")[ea]
				if ea + 1 == len(str(StockMachinenList[eachFile]).split("/")):
					open(eaThis, "w").write(eaThis)
				else:
					BlueMkDir(eaThis)

print(StockArtikelAnzahl)

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
				StockOrtList[ID]=str(Var).upper()
				BlueSave(str(VarName), str(Var).upper(), "Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
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
			print(data.split("(zKz)")[1])
			ID = int(data.split("(zKz)")[1].split("(zkz)")[0])
			Vars = str(data.split(str(ID))[1]).split("(zkz)")
			Debug("ID :  " + str(ID))
			Debug("Vars :  " + str(Vars))

			Antwort = str(ID)
			for Var in Vars:
				try:
					if Var == "Artikel":  Antwort = Antwort + " | " + str(StockArtikelList[ID])
					if Var == "Name":  Antwort = Antwort + " | " + str(StockNameList[ID])
					if Var == "Ort":  Antwort = Antwort + " | " + str(StockOrtList[ID]).upper()
					if Var == "PreisEK":  Antwort = Antwort + " | " + str(StockPreisEKList[ID])
					if Var == "PreisVKH":  Antwort = Antwort + " | " + str(StockPreisVKHList[ID])
					if Var == "PreisVK":  Antwort = Antwort + " | " + str(StockPreisVKList[ID])
					if Var == "Anzahl":  Antwort = Antwort + " | " + str(StockAnzahlList[ID])
					if Var == "Barcode":  Antwort = Antwort + " | " + str(StockBarcodeList[ID])
					if Var == "Lieferant":  Antwort = Antwort + " | " + str(StockLieferantList[ID])
				except:
					Antwort = Antwort + "None"

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
				indices = [BcodeSuche]# Bcode
			else:
				if not BarcodeSuche.rstrip() == "":# Barcode
					try: indices = [StockBarcodeList.index(BarcodeSuche)]
					except: indices = [0]
				else:
					# Artikel und Ort
					if not ArtikelSuche.rstrip() == "":
						indices = [i for i, x in enumerate(StockArtikelList) if ArtikelSuche in x][:15]
					else:
						if not OrtSuche.rstrip() == "":
							indices = [i for i, x in enumerate(StockOrtList) if OrtSuche in x][:15]
						else: indices = [0]
			try:
				Antwort = " "
				for eachDat in indices:
					Antwort = Antwort + str(eachDat) + "<K>"

			except: Debug("Nichts gefunden")
		
		Debug("Sende : " + str(Antwort))
		Antwort = Antwort.encode()
		c.send(Antwort)
c.close()
