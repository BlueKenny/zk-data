#!/usr/bin/env python3
import sys
import socket
from debug import *
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
import os
from RoundUp import *
import datetime
now = datetime.datetime.now()
from random import randint

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
AnzDAT = input("Anzahl?\n")
MaxDAT = 100000 + int(AnzDAT)
for eachFile in range(100000, MaxDAT):
	if str(eachFile)[-3] + str(eachFile)[-2] + str(eachFile)[-1] == "000": print(eachFile)
	ri = str(randint(0,99999999999))
	ri = ri.replace("0", "A")
	ri = ri.replace("1", "B")
	ri = ri.replace("2", "C")
	ri = ri.replace("3", "D")
	ri = ri.replace("4", "E")
	ri = ri.replace("5", "F")
	ri = ri.replace("6", "G")
	ri = ri.replace("7", "H")
	ri = ri.replace("8", "I")
	ri = ri.replace("9", "G")
	StockBarcodeList[eachFile]=ri
	StockArtikelList[eachFile]=ri
	StockLieferantList[eachFile]=ri
	StockNameList[eachFile]=ri
	StockOrtList[eachFile]=ri
	StockPreisEKList[eachFile]=ri
	StockPreisVKHList[eachFile]=ri
	StockPreisVKList[eachFile]=ri
	StockAnzahlList[eachFile]=ri
	StockMaschinenList[eachFile]=ri

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
			#BcodeSuche = data.split("(zKz)")[1].split("(zkz)")[0]
			#Debug("BcodeSuche : " + BcodeSuche)
			#BarcodeSuche = data.split("(zKz)")[1].split("(zkz)")[1]
			#Debug("BarcodeSuche : " + BarcodeSuche)
			#ArtikelSuche = data.split("(zKz)")[1].split("(zkz)")[2]
			#Debug("ArtikelSuche : " + ArtikelSuche)
			#OrtSuche = data.split("(zKz)")[1].split("(zkz)")[3]
			#Debug("OrtSuche : " + OrtSuche)
			#MaschineSuche = data.split("(zKz)")[1].split("(zkz)")[4]
			#Debug("MaschineSuche : " + MaschineSuche)
			SucheSuche = str(data.split("(zKz)")[1].split("(zkz)")[0])
			Debug("SucheSuche : " + SucheSuche)
			OrtSuche = data.split("(zKz)")[1].split("(zkz)")[1]
			Debug("OrtSuche : " + OrtSuche)
			MaschineSuche = data.split("(zKz)")[1].split("(zkz)")[2]
			Debug("MaschineSuche : " + MaschineSuche)
			
			indices = []
			#indices = [x for x in range(100000, 999999)] # ALLE

			# Suche Bcode
			if len(SucheSuche) == 6 and SucheSuche.isdigit():# Bcode
				Debug("Bcode")
				indices.append(int(SucheSuche))
			if len(SucheSuche) == 12 or  len(SucheSuche) == 13 and SucheSuche.isdigit():# Barcode
				Debug("Barcode")
				for counter, data in enumerate(StockBarcodeList):
					if SucheSuche == data:
						indices.append(counter)
			# Artikel
			for counter, data in enumerate(StockArtikelList):
				if SucheSuche in str(data):
					indices.append(counter)
			

			 # Bcode
			#if not BcodeSuche.rstrip() == "": indices = [BcodeSuche]; print("Rest nach Bcode " + str(indices))
			 # Barcode
			#if not BarcodeSuche.rstrip() == "" and not indices == []: indices = [counter for counter, data in enumerate(StockBarcodeList) if BarcodeSuche in data and counter in indices]; print("Rest nach Barcode " + str(indices))
			 # Artikel
			#if not ArtikelSuche.rstrip() == "" and not indices == []: indices = [counter for counter, data in enumerate(StockArtikelList) if ArtikelSuche in data and counter in indices]; print("Rest nach Artikel " + str(indices))
			 # Ort
			if not OrtSuche.rstrip() == "" and not indices == []: indices = [counter for counter, data in enumerate(StockOrtList) if OrtSuche in data and counter in indices]; print("Rest nach Ort " + str(indices))
			 # Maschine
			if not MaschineSuche.rstrip() == "" and not indices == []: indices = [counter for counter, data in enumerate(StockMaschinenList) if MaschineSuche in data and counter in indices]; print("Rest nach Maschine " + str(indices))


			indices = indices[:10]
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
