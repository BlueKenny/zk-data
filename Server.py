#!/usr/bin/env python3
import sys
import socket
from debug import *
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
import os
import datetime
now = datetime.datetime.now()

# Ordner
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

		Debug("Sende : " + str(Antwort))
		Antwort = Antwort.encode()
		c.send(Antwort)
c.close()
