#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import socket
from libs.debug import *
from libs.BlueFunc import *
import os
from libs.RoundUp import * 
import datetime
import time
import csv
from libs.barcode import *
		
def find_keys_dict(dic, val):
	"""return the keys of dictionary dic given the value"""
	dic2 = dic.copy()
	keys=[]
	while True:
		if val in dic2.values():
			key = list(dic2.keys())[list(dic2.values()).index(val)]
			keys.append(key)
			del dic2[key]
		else: break
	if len(keys) == 0: return None
	else: return keys

def find_key_dict(dic, val):
	"""return the key of dictionary dic given the value"""
	if val in dic.values():
		return list(dic.keys())[list(dic.values()).index(val)]
	else: return None

def find_value_dict(dic, key):
	"""return the value of dictionary dic given the key"""
	if val in dic.values():
		return val
	else: return None

# Ordner
DIR = ""
BlueMkDir(DIR + "Stock")
BlueMkDir(DIR + "StockBewegung")
BlueMkDir(DIR + "Kunden")
BlueMkDir(DIR + "Arbeiter")
BlueMkDir(DIR + "Import")
BlueMkDir(DIR + "Import/Preise")
#BlueMkDir(DIR + "Import/Stock")
BlueMkDir(DIR + "Import/Kunden")
BlueMkDir(DIR + "DATA")


#ArticleInfos = {"Creation": StockCreationList}

PreiseArtikelList = {}
PreiseLieferantList = {}
PreiseNameList = {}
PreisePreisEKList = {}
PreisePreisVKHList = {}
PreisePreisVKList = {}

StockCreationList = {}
StockLastChangeList = {}
StockBarcodeList = {}
StockArtikelList = {}
StockLieferantList = {}
StockNameList = {}
StockOrtList = {}
StockPreisEKList = {}
StockPreisVKHList = {}
StockPreisVKList = {}
StockAnzahlList = {}
KundeNameList = {}
KundeTelList = {}
KundeAdresseList = {}
KundeOrtList = {}

StockIDList = []
ListeDerLieferanten = []
ArbeiterListe = []
BlockedIDList= []

try:
	INDEXLIMIT = int(BlueLoad("IndexLimit", DIR + "DATA/DATA"))
except:
	INDEXLIMIT = 20
	BlueSave("IndexLimit", "20", DIR + "DATA/DATA")

#Debug("Make Cache")
#if not BlueLoad("CacheLimit", DIR + "DATA/DATA") == None:
#	MINCache = int(BlueLoad("CacheLimit", DIR + "DATA/DATA").split("-")[0])
#	MAXCache = int(BlueLoad("CacheLimit", DIR + "DATA/DATA").split("-")[1])
#else:
#	MINCache = 0
#	MAXCache = 999999
#	BlueSave("CacheLimit", "0-999999", DIR + "DATA/DATA")
#Debug("MINCache " + str(MINCache))
#Debug("MAXCache " + str(MAXCache))
#for x in range(MINCache, MAXCache):
#	StockCreationList.insert(x, "x")
#	StockLastChangeList.insert(x, "x")
#	StockBarcodeList.insert(x, "x")
#	StockArtikelList.insert(x, "x")
#	StockLieferantList.insert(x, "x")
#	StockNameList.insert(x, "x")
#	StockOrtList.insert(x, "x")
#	StockPreisEKList.insert(x, "x")
#	StockPreisVKHList.insert(x, "x")
#	StockPreisVKList.insert(x, "x")
#	StockAnzahlList.insert(x, "x")
#	KundeNameList.insert(x, "x")
#	KundeTelList.insert(x, "x")
#	KundeAdresseList.insert(x, "x")
#	KundeOrtList.insert(x, "x")

# LOAD
print("LOAD DATAbase Stock") 
StockArtikelAnzahl = 0
KundenAnzahl = 0
NeueKundenID = 10

for eachDir in os.listdir(DIR + "Stock/"):
	for eachFile in os.listdir(DIR + "Stock/" + eachDir):
		try:
			#Debug("Load Stock file " + str(eachFile))
			datei = DIR + "Stock/" + eachDir + "/" + eachFile
			eachFile = int(eachFile)
			#	ID
			StockIDList.append(eachFile)
			#	Creation
			ArticleCreation = BlueLoad("Creation", datei)
			if ArticleCreation == None or ArticleCreation == "x":
				ArticleCreation="2000-01-01"
				BlueSave("Creation", ArticleCreation, datei)
			StockCreationList[eachFile] = str(ArticleCreation)
			#	Last Change
			ArticleLastChange = BlueLoad("LastChange", datei)
			if ArticleLastChange == None or ArticleLastChange == "x":
				ArticleLastChange="2000-01-01"
				BlueSave("LastChange", ArticleLastChange, datei)
			StockLastChangeList[eachFile] = str(ArticleLastChange)
			#	Barcode
			ArticleBarcode = int(BlueLoad("Barcode", datei))
			if ArticleBarcode == None or ArticleBarcode == "x":
				ArticleBarcode = IDToBarcode(eachFile)
				BlueSave("Barcode", ArticleBarcode, datei)
			StockBarcodeList[eachFile] = int(ArticleBarcode)
			#	Article
			ArticleNumber = BlueLoad("Artikel", datei).lower()
			StockArtikelList[eachFile] = str(ArticleNumber)
			#	Supplier
			ArticleSupplier = BlueLoad("Lieferant", datei).lower()
			if ArticleSupplier == None or ArticleSupplier == "x":
				ArticleSupplier = ""
				BlueSave("Lieferant", ArticleSupplier, datei)
			StockLieferantList[eachFile] = str(ArticleSupplier)
			#	Name
			ArticleName = BlueLoad("Name", datei)
			StockNameList[eachFile] = str(ArticleName)
			#	Location
			ArticleLocation = BlueLoad("Ort", datei).upper()
			if ArticleLocation == None or ArticleLocation == "x":
				ArticleLocation = ""
				BlueSave("Ort", ArticleLocation, datei)
			StockOrtList[eachFile] = str(ArticleLocation)
			#	Cost and Prices
			
			ArticleCost=RoundUp0000(str(BlueLoad("PreisEK", datei)).replace(",", "."))
			ArticlePriceVatIncl=RoundUp05(str(BlueLoad("PreisEK", datei)).replace(",", "."))
			ArticlePriceVatExcl=RoundUp0000(float(ArticlePriceVatIncl)/1.21)
			StockPreisEKList[eachFile] = float(ArticleCost)
			StockPreisVKHList[eachFile] = float(ArticlePriceVatExcl)
			StockPreisVKList[eachFile] = float(ArticlePriceVatIncl)

			#try: StockPreisEKList[eachFile]=RoundUp0000(str(BlueLoad("PreisEK", datei)).replace(",", "."))
			#except: StockPreisEKList[eachFile] = "x"
			#try: StockPreisVKHList[eachFile]=RoundUp0000(str(BlueLoad("PreisVKH", datei)).replace(",", "."))
			#except: StockPreisVKHList[eachFile] = "x"
			#try: StockPreisVKList[eachFile]=RoundUp0000(str(BlueLoad("PreisVK", datei)).replace(",", "."))
			#except: StockPreisVKList[eachFile] = "x"

			#	Quantity
			ArticleQuantity = int(BlueLoad("Anzahl", datei))
			if ArticleQuantity == None or ArticleQuantity == "x":
				ArticleQuantity = 0
				BlueSave("Anzahl", ArticleQuantity, datei)
			StockAnzahlList[eachFile]=ArticleQuantity

			StockArtikelAnzahl = StockArtikelAnzahl  + 1
			if not StockLieferantList[eachFile] in ListeDerLieferanten: ListeDerLieferanten.append(StockLieferantList[eachFile])
		except: Debug("Failed to load")

for eachDir in os.listdir(DIR + "Kunden/"):
	for eachFile in os.listdir(DIR + "Kunden/" + eachDir):

		datei = DIR + "Kunden/" + eachDir + "/" + eachFile
		eachFile = int(eachFile)
		if eachFile > NeueKundenID: NeueKundenID = eachFile + 1
		KundeNameList[eachFile]=BlueLoad("Name", datei)
		KundeTelList[eachFile]=BlueLoad("Tel", datei)
		KundeAdresseList[eachFile]=BlueLoad("Adresse", datei)
		KundeOrtList[eachFile]=BlueLoad("Ort", datei)
	
		KundenAnzahl = KundenAnzahl  + 1

PreiseID = 0
for datei in sorted(os.listdir("Import/Preise/"), reverse=True):
	if ".csv" in datei:
		ImportDateiDATA = "Import/Preise/" + datei.replace(".csv", "")
		if os.path.exists(ImportDateiDATA):
			Debug("Preis " + str(datei))
			SearchName = BlueLoad("Name", ImportDateiDATA)
			Debug("SearchName " + str(SearchName))
			SearchArtikel = BlueLoad("Artikel", ImportDateiDATA)
			Debug("SearchArtikel " + str(SearchArtikel))
			SearchArtikel2 = BlueLoad("Artikel2", ImportDateiDATA)
			Debug("SearchArtikel2 " + str(SearchArtikel2))
			SearchArtikel3 = BlueLoad("Artikel3", ImportDateiDATA)
			Debug("SearchArtikel3 " + str(SearchArtikel3))
			SearchPreisEK = BlueLoad("PreisEK", ImportDateiDATA)
			Debug("SearchPreisEK " + str(SearchPreisEK))
			SearchPreisVKH = BlueLoad("PreisVKH", ImportDateiDATA)
			Debug("SearchPreisVKH " + str(SearchPreisVKH))
			SearchPreisVK = BlueLoad("PreisVK", ImportDateiDATA)
			Debug("SearchPreisVK " + str(SearchPreisVK))

			AnzahlDerSpalten = len(open("Import/Preise/" + datei, "r").readlines()[0].split(":"))
			IntName = 0
			IntArtikel = 0
			IntArtikel2 = 0
			IntArtikel3 = 0
			IntPreisEK = 0
			IntPreisVKH = 0
			IntPreisVK = 0
			OKName = False
			OKArtikel = False
			OKArtikel2 = False
			OKArtikel3 = False
			OKPreisEK = False
			OKPreisVKH = False 
			OKPreisVK = False

			AlleTitel = open("Import/Preise/" + datei, "r", errors="ignore").readlines()[0].split(":")
			Debug("AlleTitel " + str(AlleTitel))
			for x in range(0, AnzahlDerSpalten):
				if SearchName == AlleTitel[x]:
					IntName = x
					OKName = True
					Debug("IntName " + str(IntName))
				if SearchArtikel == AlleTitel[x]:
					IntArtikel = x
					OKArtikel = True
					Debug("IntArtikel " + str(IntArtikel))
				if SearchArtikel2 == AlleTitel[x]:
					IntArtikel2 = x
					OKArtikel2 = True
					Debug("IntArtikel2 " + str(IntArtikel2))
				if SearchArtikel3 == AlleTitel[x]:
					IntArtikel3 = x
					OKArtikel3 = True
					Debug("IntArtikel3 " + str(IntArtikel3))
				if SearchPreisEK == AlleTitel[x]:
					IntPreisEK = x
					OKPreisEK = True
					Debug("IntPreisEK " + str(IntPreisEK))
				if SearchPreisVKH == AlleTitel[x]:
					IntPreisVKH = x
					OKPreisVKH = True
					Debug("IntPreisVKH " + str(IntPreisVKH))
				if SearchPreisVK == AlleTitel[x]:
					IntPreisVK = x
					OKPreisVK = True
					Debug("IntPreisVK " + str(IntPreisVK))
			if not OKName: Debug("Kein Name")
			if not OKArtikel: Debug("Kein Artikel")
			if not OKArtikel2: Debug("Kein Artikel2")
			if not OKArtikel3: Debug("Kein Artikel3")
			if not OKPreisEK: Debug("Kein PreisEK")
			if not OKPreisVKH: Debug("Kein PreisVKH")
			if not OKPreisVK: Debug("Kein PreisVK")

			with open("Import/Preise/" + datei, "r") as csvfile:
				reader = csv.reader(csvfile, delimiter=":", quotechar="\"")
				for eachLine in reader:
					try:
						StockArtikelAnzahl = StockArtikelAnzahl  + 1
						if OKArtikel3:
							PreiseArtikelList[PreiseID] = eachLine[IntArtikel] + " " + eachLine[IntArtikel2] + " " + eachLine[IntArtikel3]
						else:
							if OKArtikel2:	
								PreiseArtikelList[PreiseID] = eachLine[IntArtikel] + " " + eachLine[IntArtikel2]
								#PreiseArtikelList.insert(PreiseID, eachLine[IntArtikel] + " " + eachLine[IntArtikel2])
							else: 
								PreiseArtikelList[PreiseID] = eachLine[IntArtikel]
								#PreiseArtikelList.insert(PreiseID, eachLine[IntArtikel])
						PreiseLieferantList[PreiseID] = datei.replace(".csv", "")
						#PreiseLieferantList.insert(PreiseID, datei.replace(".csv", ""))
						PreiseNameList[PreiseID] = eachLine[IntName]
						#PreiseNameList.insert(PreiseID, eachLine[IntName])
						## Achtung PreisVK oder PreisVKH muss drin sein !
						PreisePreisVKHList[PreiseID] = str(eachLine[IntPreisVKH]).replace(",", ".")
						#PreisePreisVKHList.insert(PreiseID, str(eachLine[IntPreisVKH]).replace(",", "."))
						PreisePreisEKList[PreiseID] = str(eachLine[IntPreisEK]).replace(",", ".")
						#PreisePreisEKList.insert(PreiseID, str(eachLine[IntPreisEK]).replace(",", "."))
						PreisePreisVKList[PreiseID] = str(eachLine[IntPreisVK]).replace(",", ".")
						#PreisePreisVKList.insert(PreiseID, str(eachLine[IntPreisVK]).replace(",", "."))
						if IntPreisVK == 0:
							PreisePreisVKList[PreiseID] = RoundUp05(float(str(PreisePreisVKHList[PreiseID]).replace(",", "."))*1.21)
							PreisePreisVKHList[PreiseID] = RoundUp0000(float(str(PreisePreisVKList[PreiseID]).replace(",", "."))/1.21)
						if IntPreisVKH == 0:
							PreisePreisVKHList[PreiseID] = RoundUp0000(float(str(PreisePreisVKList[PreiseID]).replace(",", "."))/1.21)
						if IntPreisEK == 0:
							PreisePreisEKList[PreiseID] = RoundUp0000(float(str(PreisePreisVKList[PreiseID]).replace(",", "."))*0.65)
						PreisePreisVKList[PreiseID] = RoundUp05(PreisePreisVKList[PreiseID])
						PreisePreisVKHList[PreiseID] = RoundUp0000(float(PreisePreisVKList[PreiseID])/1.21)

						PreiseID = PreiseID + 1
					except: Debug("Linie ist ungültig \n" + str(eachLine))
					

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
	try: ipname = socket.gethostbyaddr(addr[0])
	except: ipname = ["nix"]
	Debug("Verbunden mit " + str(ipname[0]))
	while True:
		DATA = c.recv(2048)
		if not DATA:
			Debug("Client sendet nicht mehr")
			break
		DATA = DATA.decode()
		Debug("DATA : " + DATA)

		mode = DATA.split("(zKz)")[0]

		Antwort = "x"

		if mode == "StockGetBewegung":
			Debug("Mode : " + mode)
			ID = int(DATA.split("(zKz)")[1].split("(zkz)")[0])
			Debug("ID : " + str(ID))
			
			DATA = []
			for Jahr in sorted(os.listdir("StockBewegung/")):
				for Monat in sorted(os.listdir("StockBewegung/" + str(Jahr))):
					for Dateiname in sorted(os.listdir("StockBewegung/" + str(Jahr) + "/" + str(Monat))):
						Datei = "StockBewegung/" + str(Jahr) + "/" + str(Monat) + "/" + Dateiname
						FirstLine = open(Datei, "r").readlines()[0]
						for eachLine in open(Datei, "r").readlines():
							if not eachLine == FirstLine and eachLine.split(":")[0] == str(ID):
								DATA.append(Jahr + Monat + Dateiname.replace(".csv", "") + "|" + eachLine.split(":")[2])
			Antwort=str(DATA)


		if mode == "StockSetBCode":
			Debug("Mode : " + mode)
			ID = 100000
			while True:
				if not ID in StockIDList and not ID in BlockedIDList:
					BlockedIDList.append(ID)
					break
				else: ID = ID + 1
			Antwort = str(ID)

		if mode == "SaveArbeiterLinie":
			Debug("Mode : " + mode)
			Arbeiter = str(DATA.split("(zKz)")[1].split("(zkz)")[0])
			Linie = str(DATA.split("(zKz)")[1].split("(zkz)")[1])
			Text = str(DATA.split("(zKz)")[1].split("(zkz)")[2])
			BlueSave(Linie, Text, "Arbeiter/" + Arbeiter)
		if mode == "GetArbeiterLinie":
			Debug("Mode : " + mode)
			Arbeiter = str(DATA.split("(zKz)")[1].split("(zkz)")[0])
			Linie = str(DATA.split("(zKz)")[1].split("(zkz)")[1])
			Antwort = str(BlueLoad(Linie, "Arbeiter/" + Arbeiter))
			

		if mode == "ListeDerArbeiter":
			Debug("Mode : " + mode)
			AntwortArbeiterListe = ""
			for each in ArbeiterListe: AntwortArbeiterListe = AntwortArbeiterListe + "|" + each
			Antwort = AntwortArbeiterListe


		if mode == "StockSetArtInfo":
			Debug("Mode : " + mode)
			ID = int(DATA.split("(zKz)")[1].split("(zkz)")[0])
			VarName = str(DATA.split("(zKz)")[1].split("(zkz)")[1])
			Var = str(DATA.split("(zKz)")[1].split("(zkz)")[2])
			Debug("ID :  " + str(ID))
			Debug("VarName :  " + str(VarName))
			Debug("Var :  " + str(Var))
			BlueMkDir(DIR + "Stock/" + str(ID)[-2] + str(ID)[-1])

			BlueSave("LastChange", str(Date()), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
			StockLastChangeList[ID] = str(Date())

			if not ID in StockIDList:
				StockArtikelAnzahl = StockArtikelAnzahl  + 1 # Neuer Artikel
				BlueSave("Creation", str(Date()), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
				StockCreationList[ID] = str(Date())
				StockIDList.append(ID)

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
			ID = int(DATA.split("(zKz)")[1].split("(zkz)")[0])
			VarName = str(DATA.split("(zKz)")[1].split("(zkz)")[1])
			Var = str(DATA.split("(zKz)")[1].split("(zkz)")[2])
			Debug("ID :  " + str(ID))
			Debug("VarName :  " + str(VarName))
			Debug("Var :  " + str(Var))
			BlueMkDir("Kunden/" + str(ID)[-2] + str(ID)[-1])

			if VarName == "Name": 
				if KundeNameList[ID] == "x": KundenAnzahl = KundenAnzahl  + 1 # Neuer Kunde
				KundeNameList[ID]=str(Var)
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

		if mode == "GetArticleInfo":
			Debug("Mode : " + mode)
			print(DATA.split("(zKz)")[1])
			
		if mode == "StockGetArtInfo":
			Debug("Mode : " + mode)
			print(DATA.split("(zKz)")[1])
			ID = DATA.split("(zKz)")[1].split("(zkz)")[0]
			Vars = str(DATA.split(str(ID))[1]).split("(zkz)")
			Debug("ID :  " + str(ID))
			Debug("Vars :  " + str(Vars))

			Antwort = str(ID)

			if not "P" in ID:
				ID = int(ID)
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
			else:
				ID = int(ID.replace("P", ""))
				for Var in Vars:
					try:
						if Var == "Artikel":  Antwort = Antwort + " | " + str(PreiseArtikelList[ID])
						if Var == "Name":  Antwort = Antwort + " | " + str(PreiseNameList[ID])
						if Var == "PreisEK":  Antwort = Antwort + " | " + str(PreisePreisEKList[ID])
						if Var == "PreisVKH":  Antwort = Antwort + " | " + str(PreisePreisVKHList[ID])
						if Var == "PreisVK":  Antwort = Antwort + " | " + str(PreisePreisVKList[ID])
						if Var == "Lieferant":  Antwort = Antwort + " | " + str(PreiseLieferantList[ID])
					except:
						Antwort = Antwort + "None"

		if mode == "KundeGetInfo":
			Debug("Mode : " + mode)
			print(DATA.split("(zKz)")[1])
			ID = int(DATA.split("(zKz)")[1].split("(zkz)")[0])
			Vars = str(DATA.split(str(ID))[1]).split("(zkz)")
			Debug("ID :  " + str(ID))
			Debug("Vars :  " + str(Vars))

			Antwort = str(ID)
			for Var in Vars:
				try:
					if Var == "Name":  Antwort = Antwort + " | " + str(KundeVornameList[ID]).title()
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
			BcodeSuche = int(DATA.split("(zKz)")[1].split("(zkz)")[0])
			Debug("BcodeSuche : " + str(BcodeSuche))
			NewStock = DATA.split("(zKz)")[1].split("(zkz)")[1]
			Debug("NewStock : " + NewStock)
			AltStock = str(StockAnzahlList[BcodeSuche])
			Debug("AltStock : " + AltStock )
			StockAnzahlList[BcodeSuche] = int(AltStock) + int(NewStock)
			BlueSave("Anzahl", StockAnzahlList[BcodeSuche], "Stock/" + str(BcodeSuche)[-2] + str(BcodeSuche)[-1] + "/" + str(BcodeSuche))

			
			BlueSave("LastChange", str(Date()), DIR + "Stock/" + str(BcodeSuche)[-2] + str(BcodeSuche)[-1] + "/" + str(BcodeSuche))
			StockLastChangeList[BcodeSuche] = str(Date())
			
			BlueMkDir(DIR + "StockBewegung/" + str(Date()).split("-")[0])
			BlueMkDir(DIR + "StockBewegung/" + str(Date()).split("-")[0] + "/" + str(Date()).split("-")[1])
			DateiStockBewegung = DIR + "StockBewegung/" + str(Date()).split("-")[0] + "/" + str(Date()).split("-")[1] + "/" + str(Date()).split("-")[2] + ".csv"
			if not os.path.exists(DateiStockBewegung): open(DateiStockBewegung, "a").write("ID:QUANTITY FROM:QUANTITY TO:COST:PRICE VAT INCL.:PRICE VAT EXCL.:MODE:USER\n")
			open(DateiStockBewegung, "a").write(str(BcodeSuche) + ":" + str(AltStock) + ":" + str(StockAnzahlList[BcodeSuche]) + ":" + str(StockPreisEKList[BcodeSuche]) + ":" + str(StockPreisVKHList[BcodeSuche]) + ":" + str(StockPreisVKList[BcodeSuche]) + ":MISC:" + str(ipname[0]) + "\n")

		if mode == "SearchStock":
			Debug("Mode : " + mode)
			SucheSuche = str(DATA.split("(zKz)")[1].split("(zkz)")[0])
			Debug("SucheSuche : " + SucheSuche)
			OrtSuche = DATA.split("(zKz)")[1].split("(zkz)")[1]
			Debug("OrtSuche : " + OrtSuche)
			LieferantSuche = DATA.split("(zKz)")[1].split("(zkz)")[2]
			Debug("LieferantSuche : " + LieferantSuche)

			indices = []
			#	ID		only 1 is possible 
			if len(SucheSuche) == 6:
				try:
					if int(SucheSuche) in StockIDList:
						indices.append(int(SucheSuche)) 
				except: Debug("Search is not an ID")

			#	Barcode		only 1 is possible
			if len(SucheSuche) == 13:# Only Barcodes with 13 integers
				try:
					ID = find_key_dict(StockBarcodeList, int(SucheSuche))
					if not ID in indices: indices.append(ID)
				except: Debug("Search is not a Barcode")
			#	Article		multiple choice possible
			ListOfArticles = find_keys_dict(StockArtikelList, str(SucheSuche))
			if not ListOfArticles == None:
				for ID in ListOfArticles:
					if not ID in indices: indices.append(ID)
			#	PArticle		multiple choice possible
			ListOfArticles = find_keys_dict(PreiseArtikelList, str(SucheSuche))
			if not ListOfArticles == None:
				for ID in ListOfArticles:
					ID = "P" + str(ID)
					if not ID in indices: indices.append(ID)
			#	Location		multiple choice possible
			if not OrtSuche == "":
				indices2 = indices
				indices = []
				ListOfLocations = find_keys_dict(StockOrtList, str(OrtSuche).upper())
				if not ListOfLocations == None:
					for ID in ListOfLocations:
						if ID in indices2: indices.append(ID)
			#	Supplier		multiple choice possible
			if not LieferantSuche == "":
				indices2 = indices
				indices = []
				ListOfSupplier = find_keys_dict(StockLieferantList, str(LieferantSuche).lower())
				if not ListOfSupplier == None:
					for ID in ListOfSupplier:
						if ID in indices2: indices.append(ID)


			indices = indices[:INDEXLIMIT]
			if indices == []: indices = [0]
		
			try:
				Antwort = " "
				for eachDat in indices:
					Antwort = Antwort.rstrip() + str(eachDat) + "<K>"

			except: Debug("Nichts gefunden")

		if mode == "SearchStockOld":
			Debug("Mode : " + mode)
			SucheSuche = str(DATA.split("(zKz)")[1].split("(zkz)")[0])
			Debug("SucheSuche : " + SucheSuche)
			OrtSuche = DATA.split("(zKz)")[1].split("(zkz)")[1]
			Debug("OrtSuche : " + OrtSuche)
			LieferantSuche = DATA.split("(zKz)")[1].split("(zkz)")[2]
			Debug("LieferantSuche : " + LieferantSuche)
			
			indices = []

			# Suche Bcode
			if len(SucheSuche) == 6 and SucheSuche.isdigit():# Bcode
				Debug("Bcode")
				indices.append(int(SucheSuche))
			if len(SucheSuche) == 12 or  len(SucheSuche) == 13 and SucheSuche.isdigit():# Barcode
				Debug("Barcode")
				for counter, DATA in enumerate(StockBarcodeList):
					if SucheSuche == str(DATA):
						indices.append(counter)
			# Artikel
			for counter, DATA in enumerate(StockArtikelList):
				if SucheSuche in str(DATA):
					if len(str(counter)) == 6:indices.append(counter)
			# Artikel PreisVorschlag
			for counter, DATA in enumerate(PreiseArtikelList):
				if SucheSuche in str(DATA):
					indices.append("P" + str(counter))
			
			 # Ort
			if not OrtSuche.rstrip() == "" and not indices == []:
				indices = [counter for counter, DATA in enumerate(StockOrtList) if OrtSuche in DATA and counter in indices]; print("Rest nach Ort " + str(indices))

			 # Lieferant
			if not LieferantSuche.rstrip() == "" and not indices == []:
				indices = [counter for counter, DATA in enumerate(StockLieferantList) if LieferantSuche.lower() in DATA.lower() and counter in indices]; print("Rest nach Lieferant " + str(indices))

			indices = indices[:INDEXLIMIT]
			if indices == []: indices = [0]
		
			try:
				Antwort = " "
				for eachDat in indices:
					Antwort = Antwort.rstrip() + str(eachDat) + "<K>"

			except: Debug("Nichts gefunden")

		if mode == "SearchKunde":
			Debug("Mode : " + mode)
			SucheSuche = str(DATA.split("(zKz)")[1].split("(zkz)")[0])
			Debug("SucheSuche : " + SucheSuche)
			TelSuche = DATA.split("(zKz)")[1].split("(zkz)")[1]
			Debug("TelSuche : " + TelSuche)
			OrtSuche = DATA.split("(zKz)")[1].split("(zkz)")[2]
			Debug("OrtSuche : " + OrtSuche)
			
			indices = []

			
			# Suche Kundennummer
			if SucheSuche.isdigit():
				Debug("Kundennummer")
				indices.append(int(SucheSuche))

			if not SucheSuche == "":
				for counter, DATA in enumerate(KundeNameList):
					if SucheSuche.lower() in str(DATA).lower() and not counter in indices:
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
