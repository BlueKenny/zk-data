#!/usr/bin/env python3
import sys
import socket
from debug import *
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
import os
from RoundUp import * 
import datetime

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
StockMaschinenList = []

ListeDerLieferanten = []
ListeDerMaschinen = []

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
	StockMaschinenList.insert(x, "x")

# LOAD
print("LOAD Database Stock") 
StockArtikelAnzahl = 0
for eachDir in os.listdir("Stock/"):
	for eachFile in os.listdir("Stock/" + eachDir):
		datei = "Stock/" + eachDir + "/" + eachFile
		eachFile = int(eachFile)

		if not BlueLoad("Barcode", datei) == None: StockBarcodeList[eachFile]=BlueLoad("Barcode", datei)
		StockArtikelList[eachFile]=BlueLoad("Artikel", datei)
		StockLieferantList[eachFile]=BlueLoad("Lieferant", datei).lower()
		StockNameList[eachFile]=BlueLoad("Name", datei)
		if not BlueLoad("Ort", datei) == None: StockOrtList[eachFile]=str(BlueLoad("Ort", datei)).upper()
		StockPreisEKList[eachFile]=BlueLoad("PreisEK", datei)
		StockPreisVKHList[eachFile]=BlueLoad("PreisVKH", datei)
		StockPreisVKList[eachFile]=BlueLoad("PreisVK", datei)
		StockAnzahlList[eachFile]=BlueLoad("Anzahl", datei)
		if not BlueLoad("Maschinen", datei) == None and not BlueLoad("Maschinen", datei) == "": StockMaschinenList[eachFile]=BlueLoad("Maschinen", datei)

		StockArtikelAnzahl  = StockArtikelAnzahl  + 1
		if not StockLieferantList[eachFile] in ListeDerLieferanten: ListeDerLieferanten.append(StockLieferantList[eachFile])
		if not StockMaschinenList[eachFile] in ListeDerMaschinen and not StockMaschinenList[eachFile] == "x": ListeDerMaschinen.append(StockMaschinenList[eachFile])

print("StockArtikelAnzahl : " + str(StockArtikelAnzahl))
print("ListeDerLieferanten : " + str(ListeDerLieferanten))
print("ListeDerMaschinen : " + str(ListeDerMaschinen))
LenListeDerMaschinen = str(len(ListeDerMaschinen))
print("LenListeDerMaschinen : " + str(LenListeDerMaschinen))

SERVER_IP = ("", 10000)
s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try: s.bind(SERVER_IP)
except: print("Server Port schon gebunden")
s.listen(1)

def Date():
	now = datetime.datetime.now()
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

		mode = data.split("(zKz)")[0]

		Antwort = "x"

		if mode == "StockSetArtInfo":
			Debug("Mode : " + mode)
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
			if VarName == "Maschinen":  
				StockMaschinenList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), "Stock/" + str(ID)[-3] + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
				if not StockMaschinenList[ID] in ListeDerMaschinen and not StockMaschinenList[ID] == "x": ListeDerMaschinen.append(StockMaschinenList[ID])

		if mode == "StockGetArtInfo":
			Debug("Mode : " + mode)
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
					if Var == "Maschinen":  Antwort = Antwort + " | " + str(StockMaschinenList[ID])
				except:
					Antwort = Antwort + "None"
		
		if mode == "GetMaschine":
			Debug("Mode : " + mode)
			MaschineIndex = int(data.split("(zKz)")[1].split("(zkz)")[0])
			Debug("MaschineIndex : " + str(MaschineIndex))
			Antwort = str((ListeDerMaschinen[MaschineIndex]))

		if mode == "GetMaschinenAnzahl":
			Debug("Mode : " + mode)
			Antwort = str(LenListeDerMaschinen)

		if mode == "GetStockZahl":
			Debug("Mode : " + mode)
			Antwort = str(StockArtikelAnzahl)

		if mode == "ChangeStock":
			Debug("Mode : " + mode)
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
			Debug("Mode : " + mode)
			SucheSuche = str(data.split("(zKz)")[1].split("(zkz)")[0])
			Debug("SucheSuche : " + SucheSuche)
			OrtSuche = data.split("(zKz)")[1].split("(zkz)")[1]
			Debug("OrtSuche : " + OrtSuche)
			LieferantSuche = data.split("(zKz)")[1].split("(zkz)")[2]
			Debug("LieferantSuche : " + LieferantSuche)
			MaschineSuche = data.split("(zKz)")[1].split("(zkz)")[3]
			Debug("MaschineSuche : " + MaschineSuche)
			
			#indices = [x for x in range(100000, 999999)] # ALLE
			#indices = pool.map(FuncSucheBarcode, indices)


			indices = []
			#indices = [x for x in range(100000, 999999)] # ALLE

			# Suche Bcode
			if len(SucheSuche) == 6 and SucheSuche.isdigit():# Bcode
				Debug("Bcode")
				indices.append(int(SucheSuche))
			if len(SucheSuche) == 12 or  len(SucheSuche) == 13 and SucheSuche.isdigit():# Barcode
				Debug("Barcode")
				for counter, data in enumerate(StockBarcodeList):
					if SucheSuche == str(data):
						indices.append(counter)
			# Artikel
			for counter, data in enumerate(StockArtikelList):
				if SucheSuche in str(data):
					indices.append(counter)
			
			 # Ort
			if not OrtSuche.rstrip() == "" and not indices == []: indices = [counter for counter, data in enumerate(StockOrtList) if OrtSuche in data and counter in indices]; print("Rest nach Ort " + str(indices))

			 # Lieferant
			if not LieferantSuche.rstrip() == "" and not indices == []: indices = [counter for counter, data in enumerate(StockLieferantList) if LieferantSuche in data and counter in indices]; print("Rest nach Lieferant " + str(indices))

			 # Maschine
			if not MaschineSuche.rstrip() == "" and not indices == []: indices = [counter for counter, data in enumerate(StockMaschinenList) if MaschineSuche in data and counter in indices]; print("Rest nach Maschine " + str(indices))


			indices = indices[:50]
			if indices == []: indices = [0]
		
			try:
				Antwort = " "
				for eachDat in indices:
					Antwort = Antwort.rstrip() + str(eachDat) + "<K>"

			except: Debug("Nichts gefunden")
		
		Debug("Sende : " + str(Antwort))
		Antwort = Antwort.encode()
		c.send(Antwort)
c.close()
