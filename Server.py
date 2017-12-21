#!/usr/bin/env python3
import sys
import socket
from debug import *
from BlueFunc import BlueMkDir, BlueLenDatei, BlueLoad, BlueSave
import os
from RoundUp import * 
import datetime
import time

SlowDownFaktor = 0
# Ordner
DIR = ""
#DIR = "/home/phablet/.local/share/zk-data.bluekenny/"
#BlueMkDir(DIR)
BlueMkDir(DIR + "Stock")
BlueMkDir(DIR + "StockBewegung")
BlueMkDir(DIR + "Kunden")
BlueMkDir(DIR + "Arbeiter")

StockCreationList = []
StockLastChangeList = []
StockBarcodeList = []
StockArtikelList = []
StockLieferantList = []
StockNameList = []
StockOrtList = []
StockPreisEKList = []
StockPreisVKHList = []
StockPreisVKList = []
StockAnzahlList = []
ListeDerLieferanten = []
KundeVornameList = []
KundeNachnameList = []
KundeTelList = []
KundeAdresseList = []
KundeOrtList = []
ArbeiterListe = []

try:
	INDEXLIMIT = int(BlueLoad("IndexLimit", DIR + "DATA"))
except:
	INDEXLIMIT = 20
	BlueSave("IndexLimit", "20", DIR + "DATA")

Debug("Make Cache")
if not BlueLoad("CacheLimit", DIR + "DATA") == None:
	MINCache = int(BlueLoad("CacheLimit", DIR + "DATA").split("-")[0])
	MAXCache = int(BlueLoad("CacheLimit", DIR + "DATA").split("-")[1])
else:
	MINCache = 0
	MAXCache = 999999
	BlueSave("CacheLimit", "0-999999", DIR + "DATA")
Debug("MINCache " + str(MINCache))
Debug("MAXCache " + str(MAXCache))
for x in range(MINCache, MAXCache):
	StockCreationList.insert(x, "x")
	StockLastChangeList.insert(x, "x")
	StockBarcodeList.insert(x, "x")
	StockArtikelList.insert(x, "x")
	StockLieferantList.insert(x, "x")
	StockNameList.insert(x, "x")
	StockOrtList.insert(x, "x")
	StockPreisEKList.insert(x, "x")
	StockPreisVKHList.insert(x, "x")
	StockPreisVKList.insert(x, "x")
	StockAnzahlList.insert(x, "x")
	KundeVornameList.insert(x, "x")
	KundeNachnameList.insert(x, "x")
	KundeTelList.insert(x, "x")
	KundeAdresseList.insert(x, "x")
	KundeOrtList.insert(x, "x")

# LOAD
print("LOAD Database Stock") 
StockArtikelAnzahl = 0
KundenAnzahl = 0
NeueKundenID = 10
for eachDir in os.listdir(DIR + "Stock/"):
	for eachFile in os.listdir(DIR + "Stock/" + eachDir):

		datei = DIR + "Stock/" + eachDir + "/" + eachFile
		eachFile = int(eachFile)
	
		if BlueLoad("Creation", datei) == None: BlueSave("Creation", "x", datei)
		StockCreationList[eachFile]=BlueLoad("Creation", datei)

		if BlueLoad("LastChange", datei) == None: BlueSave("LastChange", "x", datei)
		StockLastChangeList[eachFile]=BlueLoad("LastChange", datei)

		if BlueLoad("Barcode", datei) == None: BlueSave("Barcode", "x", datei)
		StockBarcodeList[eachFile]=BlueLoad("Barcode", datei)

		StockArtikelList[eachFile]=BlueLoad("Artikel", datei)
		if BlueLoad("Lieferant", datei) == None: BlueSave("Lieferant", "x", datei)
		StockLieferantList[eachFile]=BlueLoad("Lieferant", datei).lower()
		StockNameList[eachFile]=BlueLoad("Name", datei)
		if BlueLoad("Ort", datei) == None: BlueSave("Ort", "x", datei)
		StockOrtList[eachFile]=str(BlueLoad("Ort", datei)).upper()
		StockPreisEKList[eachFile]=BlueLoad("PreisEK", datei)
		StockPreisVKHList[eachFile]=BlueLoad("PreisVKH", datei)
		StockPreisVKList[eachFile]=BlueLoad("PreisVK", datei)
		StockAnzahlList[eachFile]=BlueLoad("Anzahl", datei)

		StockArtikelAnzahl = StockArtikelAnzahl  + 1
		if not StockLieferantList[eachFile] in ListeDerLieferanten: ListeDerLieferanten.append(StockLieferantList[eachFile])

for eachDir in os.listdir(DIR + "Kunden/"):
	for eachFile in os.listdir(DIR + "Kunden/" + eachDir):

		datei = DIR + "Kunden/" + eachDir + "/" + eachFile
		eachFile = int(eachFile)
		if eachFile > NeueKundenID: NeueKundenID = eachFile + 1
		KundeVornameList[eachFile]=BlueLoad("Vorname", datei)
		KundeNachnameList[eachFile]=BlueLoad("Nachname", datei)
		KundeTelList[eachFile]=BlueLoad("Tel", datei)
		KundeAdresseList[eachFile]=BlueLoad("Adresse", datei)
		KundeOrtList[eachFile]=BlueLoad("Ort", datei)
	
		KundenAnzahl = KundenAnzahl  + 1

for Arbeiter in os.listdir(DIR + "Arbeiter"):
	ArbeiterListe.append(Arbeiter)
if len(ArbeiterListe) == 0: ArbeiterListe.append("Arbeiter1")

print("StockArtikelAnzahl : " + str(StockArtikelAnzahl))
print("ListeDerLieferanten : " + str(ListeDerLieferanten))
print("KundenAnzahl : " + str(KundenAnzahl))
print("NeueKundenID : " + str(NeueKundenID))


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
	ipname = socket.gethostbyaddr(addr[0])
	Debug("Verbunden mit " + str(ipname[0]))
	while True:
		data = c.recv(2048)
		if not data:
			Debug("Client sendet nicht mehr")
			break
		data = data.decode()
		Debug("Data : " + data)

		if not SlowDownFaktor == 0: time.sleep(SlowDownFaktor)
		mode = data.split("(zKz)")[0]

		Antwort = "x"
		
		if mode == "ListeDerArbeiter":
			Debug("Mode : " + mode)
			AntwortArbeiterListe = ""
			for each in ArbeiterListe: AntwortArbeiterListe = AntwortArbeiterListe + "|" + each
			Antwort = AntwortArbeiterListe


		if mode == "StockSetArtInfo":
			Debug("Mode : " + mode)
			ID = int(data.split("(zKz)")[1].split("(zkz)")[0])
			VarName = str(data.split("(zKz)")[1].split("(zkz)")[1])
			Var = str(data.split("(zKz)")[1].split("(zkz)")[2])
			Debug("ID :  " + str(ID))
			Debug("VarName :  " + str(VarName))
			Debug("Var :  " + str(Var))
			BlueMkDir(DIR + "Stock/" + str(ID)[-2] + str(ID)[-1])

			BlueSave("LastChange", str(Date()), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			StockLastChangeList[ID] = str(Date())

			if VarName == "Barcode": 
				StockBarcodeList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Artikel": 
				StockArtikelList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Lieferant": 
				StockLieferantList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
				if not StockLieferantList[ID] in ListeDerLieferanten: ListeDerLieferanten.append(StockLieferantList[ID]) # Neuer Artikel
			if VarName == "Name":  
				if StockNameList[ID] == "x":
					StockArtikelAnzahl = StockArtikelAnzahl  + 1 # Neuer Artikel
					BlueSave("Creation", str(Date()), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
					StockCreationList[ID] = str(Date())
				StockNameList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Ort":  
				StockOrtList[ID]=str(Var).upper()
				BlueSave(str(VarName), str(Var).upper(), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "PreisEK":  
				StockPreisEKList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "PreisVKH":  
				StockPreisVKHList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "PreisVK":  
				StockPreisVKList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Anzahl":  
				StockAnzahlList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))

		if mode == "KundeSetInfo":
			Debug("Mode : " + mode)
			ID = int(data.split("(zKz)")[1].split("(zkz)")[0])
			VarName = str(data.split("(zKz)")[1].split("(zkz)")[1])
			Var = str(data.split("(zKz)")[1].split("(zkz)")[2])
			Debug("ID :  " + str(ID))
			Debug("VarName :  " + str(VarName))
			Debug("Var :  " + str(Var))
			BlueMkDir("Kunden/" + str(ID)[-2] + str(ID)[-1])

			if VarName == "Vorname": 
				KundeVornameList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Kunden/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Nachname": 
				if KundeNachnameList[ID] == "x": KundenAnzahl = KundenAnzahl  + 1 # Neuer Kunde
				KundeNachnameList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Kunden/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Tel": 
				KundeTelList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Kunden/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Adresse":
				KundeAdresseList[ID]=str(Var)
				BlueSave(str(VarName), str(Var), DIR + "Kunden/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			if VarName == "Ort":  
				KundeOrtList[ID]=str(Var).upper()
				BlueSave(str(VarName), str(Var).upper(), DIR + "Kunden/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))

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
					if Var == "LastChange":  Antwort = Antwort + " | " + str(StockLastChangeList[ID])
					if Var == "Creation":  Antwort = Antwort + " | " + str(StockCreationList[ID])
					if Var == "Lieferant":  Antwort = Antwort + " | " + str(StockLieferantList[ID])
				except:
					Antwort = Antwort + "None"

		if mode == "KundeGetInfo":
			Debug("Mode : " + mode)
			print(data.split("(zKz)")[1])
			ID = int(data.split("(zKz)")[1].split("(zkz)")[0])
			Vars = str(data.split(str(ID))[1]).split("(zkz)")
			Debug("ID :  " + str(ID))
			Debug("Vars :  " + str(Vars))

			Antwort = str(ID)
			for Var in Vars:
				try:
					if Var == "Vorname":  Antwort = Antwort + " | " + str(KundeVornameList[ID]).title()
					if Var == "Nachname":  Antwort = Antwort + " | " + str(KundeNachnameList[ID]).title()
					if Var == "Tel":  Antwort = Antwort + " | " + str(KundeTelList[ID])
					if Var == "Adresse":  Antwort = Antwort + " | " + str(KundeAdresseList[ID]).title()
					if Var == "Ort":  Antwort = Antwort + " | " + str(KundeOrtList[ID]).title()
				except:
					Antwort = Antwort + "None"
		
		if mode == "GetStockZahl":
			Debug("Mode : " + mode)
			Antwort = str(StockArtikelAnzahl)

		if mode == "GetKundenZahl":
			Debug("Mode : " + mode)
			Antwort = str(KundenAnzahl)

		if mode == "NeueKundenID":
			Debug("Mode : " + mode)
			while True:
				Debug("NeueKundenID: " + str(NeueKundenID))
				if not os.path.exists(DIR + "Kunden/" + str(NeueKundenID)[-2] + str(NeueKundenID)[-1] + "/" + str(NeueKundenID)): break
				NeueKundenID = NeueKundenID + 1
			Antwort = str(NeueKundenID)

		if mode == "ChangeStock":
			Debug("Mode : " + mode)
			BcodeSuche = int(data.split("(zKz)")[1].split("(zkz)")[0])
			Debug("BcodeSuche : " + str(BcodeSuche))
			NewStock = data.split("(zKz)")[1].split("(zkz)")[1]
			Debug("NewStock : " + NewStock)
			AltStock = str(StockAnzahlList[BcodeSuche])
			Debug("AltStock : " + AltStock )
			StockAnzahlList[BcodeSuche] = int(AltStock) + int(NewStock)
			BlueSave("Anzahl", StockAnzahlList[BcodeSuche], "Stock/" + str(BcodeSuche)[-2] + str(BcodeSuche)[-1] + "/" + str(BcodeSuche))

			BlueMkDir(DIR + "StockBewegung/" + str(Date()).split("-")[0])
			BlueMkDir(DIR + "StockBewegung/" + str(Date()).split("-")[0] + "/" + str(Date()).split("-")[1])
			DateiStockBewegung = DIR + "StockBewegung/" + str(Date()).split("-")[0] + "/" + str(Date()).split("-")[1] + "/" + str(Date()).split("-")[2]
			open(DateiStockBewegung, "a").write("\n" + str(BcodeSuche) + " from " + str(AltStock) + " to " + str(StockAnzahlList[BcodeSuche]))

		if mode == "SearchStock":
			Debug("Mode : " + mode)
			SucheSuche = str(data.split("(zKz)")[1].split("(zkz)")[0])
			Debug("SucheSuche : " + SucheSuche)
			OrtSuche = data.split("(zKz)")[1].split("(zkz)")[1]
			Debug("OrtSuche : " + OrtSuche)
			LieferantSuche = data.split("(zKz)")[1].split("(zkz)")[2]
			Debug("LieferantSuche : " + LieferantSuche)
			
			indices = []

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


			indices = indices[:INDEXLIMIT]
			if indices == []: indices = [0]
		
			try:
				Antwort = " "
				for eachDat in indices:
					Antwort = Antwort.rstrip() + str(eachDat) + "<K>"

			except: Debug("Nichts gefunden")

		if mode == "SearchKunde":
			Debug("Mode : " + mode)
			SucheSuche = str(data.split("(zKz)")[1].split("(zkz)")[0])
			Debug("SucheSuche : " + SucheSuche)
			TelSuche = data.split("(zKz)")[1].split("(zkz)")[1]
			Debug("TelSuche : " + TelSuche)
			OrtSuche = data.split("(zKz)")[1].split("(zkz)")[2]
			Debug("OrtSuche : " + OrtSuche)
			
			indices = []

			
			# Suche Kundennummer
			if SucheSuche.isdigit():
				Debug("Kundennummer")
				indices.append(int(SucheSuche))

			if not SucheSuche == "":
				for NameTeil in SucheSuche.split(" "):
					NameTeil = NameTeil.lower()
					for counter, data in enumerate(KundeVornameList):
						if NameTeil in str(data).lower() and not counter in indices:
							indices.append(counter)
					for counter, data in enumerate(KundeNachnameList):
						if NameTeil in str(data).lower() and not counter in indices:
							indices.append(counter)

			indices = indices[:INDEXLIMIT]
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
