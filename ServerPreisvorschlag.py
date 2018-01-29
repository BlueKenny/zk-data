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

SERVER_PORT=10001

def find_keys_dict(dic, val):
    """return the keys of dictionary dic given the value"""
    dic2 = dic.copy()
    keys=[]
    while True:
        if val in dic2.values():
            #for key in list(dic2.keys()):
            #	for eachpart in dic2[key].split(" "):
            #		if val == eachpart and not key in keys:
            #			keys.append(key)
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
    if key in dic:
        return dic[key]
    else: return None

# Ordner
DIR = ""
BlueMkDir("Import")
BlueMkDir("Import/Preise")
BlueMkDir("DATA")


PreiseArtikelList = {}
PreiseArtikel2List = {}
PreiseArtikel3List = {}
PreiseLieferantList = {}
PreiseLieferantMitDatumList = {}
PreiseNameList = {}
PreisePreisEKList = {}
PreisePreisVKHList = {}
PreisePreisVKList = {}


ListeDerLieferanten = []

try:
    INDEXLIMIT = int(BlueLoad("IndexLimit", DIR + "DATA/DATA"))
except:
    INDEXLIMIT = 20
    BlueSave("IndexLimit", "20", DIR + "DATA/DATA")

# LOAD
print("Lade Preisvorschläge")
StockArtikelAnzahl = 0

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
                    if not SearchArtikel in eachLine:#try:
                        #print("eachLine : " + str(eachLine))
                        StockArtikelAnzahl = StockArtikelAnzahl  + 1


                        PreiseArtikelList[PreiseID] = eachLine[IntArtikel].upper()
                        if OKArtikel2: PreiseArtikel2List[PreiseID] = eachLine[IntArtikel2].upper()
                        else: PreiseArtikel2List[PreiseID] = ""
                        if OKArtikel3: PreiseArtikel3List[PreiseID] = eachLine[IntArtikel3].upper()
                        else: PreiseArtikel3List[PreiseID] = ""
                        PreiseLieferantList[PreiseID] = datei.replace(".csv", "").split("_")[0].upper()
                        PreiseLieferantMitDatumList[PreiseID] = datei.replace(".csv", "").upper()
                        if not PreiseLieferantList[PreiseID] in ListeDerLieferanten: ListeDerLieferanten.append(PreiseLieferantList[PreiseID])
                        PreiseNameList[PreiseID] = eachLine[IntName]
                        ## Achtung PreisVK oder PreisVKH muss drin sein !
                        PreisePreisVKHList[PreiseID] = str(eachLine[IntPreisVKH]).replace(",", ".")
                        PreisePreisEKList[PreiseID] = str(eachLine[IntPreisEK]).replace(",", ".")
                        PreisePreisVKList[PreiseID] = str(eachLine[IntPreisVK]).replace(",", ".")
                        if IntPreisVK == 0:
                            PreisePreisVKList[PreiseID] = RoundUp05(float(str(PreisePreisVKHList[PreiseID]).replace(",", "."))*1.21)
                            PreisePreisVKHList[PreiseID] = RoundUp0000(float(str(PreisePreisVKList[PreiseID]).replace(",", "."))/1.21)
                        if IntPreisVKH == 0:
                            if str(PreisePreisVKList[PreiseID]) == "": PreisePreisVKList[PreiseID] = 0
                            PreisePreisVKHList[PreiseID] = RoundUp0000(float(str(PreisePreisVKList[PreiseID]).replace(",", "."))/1.21)
                        if IntPreisEK == 0:
                            PreisePreisEKList[PreiseID] = RoundUp0000(float(str(PreisePreisVKList[PreiseID]).replace(",", "."))*0.65)
                        PreisePreisVKList[PreiseID] = RoundUp05(PreisePreisVKList[PreiseID])
                        PreisePreisVKHList[PreiseID] = RoundUp0000(float(PreisePreisVKList[PreiseID])/1.21)

                        PreiseID = PreiseID + 1
                    #except: Debug("Linie ist ungültig \n" + str(eachLine))


print("StockArtikelAnzahl : " + str(StockArtikelAnzahl))
print("ListeDerLieferanten : " + str(ListeDerLieferanten))


SERVER_IP = ("", SERVER_PORT)
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

        if mode == "GetArtInfo":
            Debug("Mode : " + mode)
            print(DATA.split("(zKz)")[1])
            ID = DATA.split("(zKz)")[1].split("(zkz)")[0]
            Vars = str(DATA.split(str(ID))[1]).split("(zkz)")
            Debug("ID :  " + str(ID))
            Debug("Vars :  " + str(Vars))

            Antwort = str(ID)

            ID = int(ID.replace("P", ""))
            for Var in Vars:
                try:
                    if Var == "Artikel":  Antwort = Antwort + " | " + str(PreiseArtikelList[ID])
                    if Var == "Artikel2":  Antwort = Antwort + " | " + str(PreiseArtikel2List[ID])
                    if Var == "Artikel3":  Antwort = Antwort + " | " + str(PreiseArtikel3List[ID])
                    if Var == "Name":  Antwort = Antwort + " | " + str(PreiseNameList[ID])
                    if Var == "PreisEK":  Antwort = Antwort + " | " + str(PreisePreisEKList[ID])
                    if Var == "PreisVKH":  Antwort = Antwort + " | " + str(PreisePreisVKHList[ID])
                    if Var == "PreisVK":  Antwort = Antwort + " | " + str(PreisePreisVKList[ID])
                    if Var == "Lieferant":  Antwort = Antwort + " | " + str(PreiseLieferantList[ID])
                    if Var == "LieferantMitDatum":  Antwort = Antwort + " | " + str(PreiseLieferantMitDatumList[ID])
                except:
                    Antwort = Antwort + "None"

        if mode == "GetStockZahl":
            Debug("Mode : " + mode)
            Antwort = str(StockArtikelAnzahl)

        if mode == "SearchStock":
            Debug("Mode : " + mode)
            SucheSuche = str(DATA.split("(zKz)")[1].split("(zkz)")[0])
            SucheSuche = SucheSuche.upper()
            Debug("SucheSuche : " + SucheSuche)
            LieferantSuche = DATA.split("(zKz)")[1].split("(zkz)")[1]
            LieferantSuche = LieferantSuche.upper()
            Debug("LieferantSuche : " + LieferantSuche)

            indices = []

            #	PArticle		multiple choice possible
            ListOfArticles = find_keys_dict(PreiseArtikelList, str(SucheSuche))
            if not ListOfArticles == None:
                for ID in ListOfArticles:
                    ID = "P" + str(ID)
                    if not ID in indices: indices.append(ID)
            #	PArticle2		multiple choice possible
            ListOfArticles = find_keys_dict(PreiseArtikel2List, str(SucheSuche))
            if not ListOfArticles == None:
                for ID in ListOfArticles:
                    ID = "P" + str(ID)
                    if not ID in indices: indices.append(ID)
            #	PArticle3		multiple choice possible
            ListOfArticles = find_keys_dict(PreiseArtikel3List, str(SucheSuche))
            if not ListOfArticles == None:
                for ID in ListOfArticles:
                    ID = "P" + str(ID)
                    if not ID in indices: indices.append(ID)
            #	Supplier		multiple choice possible
            if not LieferantSuche == "":
                #indices2 = indices
                #indices = []
                #ListOfSupplier = find_keys_dict(PreiseLieferantList, str(LieferantSuche))
                #if not ListOfSupplier == None:
                #    for ID in ListOfSupplier:
                #        if ID in indices2: indices.append(ID)
                indices2 = indices; indices = []
                for ID in indices2:
                    ID = int(ID.replace("P", ""))
                    print("PreiseLieferantList[" + str(ID) + "] " + str(PreiseLieferantList[ID]))
                    if PreiseLieferantList[ID] == str(LieferantSuche):
                        ID = "P" + str(ID)
                        indices.append(ID)

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
