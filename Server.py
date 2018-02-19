#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from libs.debug import *
from libs.BlueFunc import *
import os
from libs.RoundUp import * 
import datetime
import time
from libs.barcode import *
import json
import csv
import random
import os.path, time

import threading

SERVER_PORT=10000

StockCreationList = {}
StockLastChangeList = {}
StockBarcodeList = {}
StockArtikelList = {}
StockArtikel2List = {}
StockArtikel3List = {}
StockLieferantList = {}
StockNameList = {}
StockOrtList = {}
StockPreisEKList = {}
StockPreisVKHList = {}
StockPreisVKList = {}
StockAnzahlList = {}


try: from peewee import *
except:
    if platform.system() == "Linux": os.system("pip3 install --user peewee")

SERVER_SQL=BlueLoad("SERVERSQL", "DATA/DATA")
if SERVER_SQL == "None":
    SERVER_SQL = "127.0.0.1"
    SERVER_SQL=BlueSave("SERVERSQL", SERVER_SQL, "DATA/DATA")

from playhouse.shortcuts import model_to_dict, dict_to_model
local_db = SqliteDatabase("DATA/stock.db")
memory_db = SqliteDatabase("::memory::")

class Bewegung(Model):
    identification = CharField(primary_key = True)
    bcode = CharField(null = False)
    datum = CharField(null = False, default=str(Date()))
    start = FloatField(null = False, default=0)
    end = FloatField(null = False, default=0)
    preisek = FloatField(null = False, default = 0.0)
    preisvkh = FloatField(null = False, default = 0.0)
    preisvk = FloatField(null = False, default = 0.0)
    mode = CharField(null = False)
    user = CharField(null = False)

    class Meta:
        database = local_db

class Artikel(Model):# All Str are upper()
    identification = CharField(primary_key = True)
    name_de = CharField(default = "")
    name_fr = CharField(default = "")
    artikel = CharField(default = "")
    artikel2 = CharField(default = "")
    artikel3 = CharField(default = "")
    artikel4 = CharField(default = "")
    barcode = IntegerField(default=0)
    lieferant = CharField(default="")
    preisek = FloatField(default = 0.0)
    preisvkh = FloatField(default = 0.0)
    preisvk = FloatField(default = 0.0)
    anzahl = FloatField(default = 0.0)
    ort = CharField(default = "")
    lastchange = CharField(default=str(Timestamp()))
    creation = CharField(default=str(Date()))
    minimum = FloatField(default = 0.0)
    categorie = CharField(default = "")
    bild = CharField(default = "")
    beschreibung_de = TextField(default = "")
    beschreibung_fr = TextField(default = "")
    baujahr = IntegerField(default = 0)
    web = BooleanField(default = False)
    farbe = CharField(default = "")

    class Meta:
        database = local_db


local_db.connect()
try:
    local_db.create_tables([Artikel])
except:
    print("Artikel table exists in local_db")
local_db.close()

local_db.connect()
try:
    local_db.create_tables([Bewegung])
except:
    print("Bewegung table exists in local_db")
local_db.close()

# Ordner
DIR = ""
#BlueMkDir(DIR + "StockBewegung")
BlueMkDir(DIR + "DATA")
BlueMkDir(DIR + "Import")
BlueMkDir(DIR + "Import/Preise")

local_db.connect()
BeID = 1
while True:
    query = Bewegung.select().where(Bewegung.identification == str(BeID))
    if not query.exists():
        break
    BeID = BeID + 1
local_db.close()

try:
    INDEXLIMIT = int(BlueLoad("IndexLimit", DIR + "DATA/DATA"))
except:
    INDEXLIMIT = 50
    BlueSave("IndexLimit", INDEXLIMIT, DIR + "DATA/DATA")

# Old Load
LoadOld = False
if LoadOld:
    for eachDir in sorted(os.listdir(DIR + "Stock/")):
        print(str(eachDir) + "%")
        for eachFile in sorted(os.listdir(DIR + "Stock/" + eachDir)):
            if True:#try:
                #Debug("Load Stock file " + str(eachFile))
                datei = DIR + "Stock/" + eachDir + "/" + eachFile
                eachFile = int(eachFile)

                #	Creation
                ArticleCreation = BlueLoad("Creation", datei)
                if ArticleCreation == None or ArticleCreation == "x":
                    ArticleCreation="2000-01-01"
                    BlueSave("Creation", ArticleCreation, datei)
                StockCreationList[eachFile] = str(ArticleCreation)
                #	Last Change
                ArticleLastChange = BlueLoad("LastChange", datei)
                if ArticleLastChange == None or ArticleLastChange == "x":
                    ArticleLastChange="0.00"
                    BlueSave("LastChange", ArticleLastChange, datei)
                StockLastChangeList[eachFile] = str(ArticleLastChange)
                #	Barcode
                ArticleBarcode = str(BlueLoad("Barcode", datei))
                if ArticleBarcode == None or ArticleBarcode == "None" or ArticleBarcode == "x" or ArticleBarcode == "":
                    ArticleBarcode = IDToBarcode(eachFile)
                    BlueSave("Barcode", ArticleBarcode, datei)
                StockBarcodeList[eachFile] = int(ArticleBarcode)
                #	Article
                ArticleNumber = BlueLoad("Artikel", datei)
                if ArticleNumber == None: ArticleNumber = ""
                else: ArticleNumber = ArticleNumber.lower()
                StockArtikelList[eachFile] = str(ArticleNumber).upper()
                #	Article2
                ArticleNumber = BlueLoad("Artikel2", datei)
                if ArticleNumber == None: ArticleNumber = ""
                else: ArticleNumber = ArticleNumber.lower()
                StockArtikel2List[eachFile] = str(ArticleNumber).upper()
                #	Article3
                ArticleNumber = BlueLoad("Artikel3", datei)
                if ArticleNumber == None: ArticleNumber = ""
                else: ArticleNumber = ArticleNumber.lower()
                StockArtikel3List[eachFile] = str(ArticleNumber).upper()
                #	Supplier
                ArticleSupplier = BlueLoad("Lieferant", datei).lower()
                if ArticleSupplier == None or ArticleSupplier == "x":
                    ArticleSupplier = ""
                    BlueSave("Lieferant", ArticleSupplier, datei)
                StockLieferantList[eachFile] = str(ArticleSupplier).upper()
                #	Name
                ArticleName = BlueLoad("Name", datei)
                StockNameList[eachFile] = str(ArticleName)
                #	Location
                ArticleLocation = BlueLoad("Ort", datei)
                if ArticleLocation == None or ArticleLocation == "x":
                    ArticleLocation = ""
                    BlueSave("Ort", ArticleLocation, datei)
                StockOrtList[eachFile] = str(ArticleLocation).upper()
                #	Cost and Prices
                ArticleCost = str(BlueLoad("PreisEK", datei))
                if ArticleCost == "x" or ArticleCost == "None" or ArticleCost == "": ArticleCost = "0.00"
                ArticleCost=RoundUp0000(str(ArticleCost).replace(",", "."))
                ArticlePriceVatIncl = str(BlueLoad("PreisVK", datei))
                if ArticlePriceVatIncl == "x" or ArticlePriceVatIncl == "None" or ArticlePriceVatIncl == "": ArticlePriceVatIncl = "0.00"
                ArticlePriceVatIncl=RoundUp05(str(ArticlePriceVatIncl).replace(",", "."))
                ArticlePriceVatExcl = str(BlueLoad("PreisVKH", datei))
                ArticlePriceVatExcl=RoundUp0000(float(ArticlePriceVatIncl)/1.21)
                StockPreisEKList[eachFile] = float(ArticleCost)
                StockPreisVKHList[eachFile] = float(ArticlePriceVatExcl)
                StockPreisVKList[eachFile] = float(ArticlePriceVatIncl)

                #	Quantity
                ArticleQuantity = str(BlueLoad("Anzahl", datei))
                if ArticleQuantity == None or ArticleQuantity == "None" or ArticleQuantity == "x" or ArticleQuantity == "":
                    ArticleQuantity = 0
                    BlueSave("Anzahl", ArticleQuantity, datei)
                StockAnzahlList[eachFile]=float(ArticleQuantity)

                local_db.connect()
                query = Artikel.select().where(Artikel.identification == str(eachFile))
                if not query.exists():
                    print("Erstelle Artikel " + str(eachFile))
                    ThisArtikel = Artikel.create(creation=StockCreationList[eachFile],
                                                 lastchange=StockLastChangeList[eachFile],
                                                 barcode=StockBarcodeList[eachFile],
                                                 artikel=StockArtikelList[eachFile],
                                                 artikel2=StockArtikel2List[eachFile],
                                                 artikel3=StockArtikel3List[eachFile],
                                                 artikel4="",
                                                 lieferant=StockLieferantList[eachFile],
                                                 name_de=StockNameList[eachFile],
                                                 ort=StockOrtList[eachFile],
                                                 preisek=StockPreisEKList[eachFile],
                                                 preisvkh=StockPreisVKHList[eachFile],
                                                 preisvk=StockPreisVKList[eachFile],
                                                 anzahl=StockAnzahlList[eachFile],
                                                 minimum=0.0,
                                                 identification=str(eachFile))
                    ThisArtikel.save()
                local_db.close()
    #except: Debug("Failed to load")

    local_db.connect()
    for jedesJahr in os.listdir("StockBewegung"):
        for jedenMonat in sorted(os.listdir("StockBewegung/" + jedesJahr)):
            for jedeDatei in sorted(os.listdir("StockBewegung/" + jedesJahr + "/" + jedenMonat + "/")):
                file = "StockBewegung/" + jedesJahr + "/" + jedenMonat + "/" + jedeDatei
                for line in open(file, "r").readlines():
                    data = line.split(":")
                    ID = data[0]
                    DATUM = jedesJahr + "-" + jedenMonat + "-" + jedeDatei.replace(".csv", "")
                    if not ID == "ID":
                        query = Bewegung.select().where(Bewegung.identification == str(BeID))
                        if not query.exists():
                            print("Bewegung " + DATUM + " " + str(BeID) + " \n" + str(data))
                            ThisArtikel = Bewegung.create(identification = str(BeID),
                                                         bcode=str(ID),
                                                         datum=str(DATUM),
                                                         start=float(data[1]),
                                                         end=float(data[2]),
                                                         preisek=float(data[3]),
                                                         preisvkh=float(data[4]),
                                                         preisvk=float(data[5]),
                                                         mode=str(data[6]),
                                                         user=str(data[7]).rstrip())
                            ThisArtikel.save()
                        BeID = BeID + 1
    local_db.close()

# LOAD
print("LOAD DATAbase Stock")

SERVER_IP = ("", SERVER_PORT)
s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try: s.bind(SERVER_IP)
except: print("Server Port schon gebunden")
s.listen(1)

def Date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")

def Timestamp():
    return time.time()

def SavePreisvorschlag(List):
    #print("Geladene daten werden in die datenbank importiert")
    Artikel.insert_many(List).execute()

def Preisvorschlag():
    print("Preisvorschläge werden geladen")
    for ImportDatei in os.listdir("Import/Preise/"):
        if ".csv" in ImportDatei:
            ImportDatei = "Import/Preise/" + ImportDatei
            ImportData = ImportDatei[:-4]
            LieferantName = ImportData.split("/")[2].upper()
            print(ImportDatei)
            NewLastChange = str(time.ctime(os.path.getmtime(ImportDatei)))
            OldLastChange = str(BlueLoad("LastChange", ImportData))

            if not NewLastChange == OldLastChange:
                print("RELOAD " + str(ImportData))
                memory_db.connect()
                Artikel.delete().where(Artikel.lieferant == LieferantName).execute()

                DictOfPos = {}
                ErsteLinie = open(ImportDatei, "r", errors="ignore").readlines()[0]
                for each in ErsteLinie.split(":"):
                    DictOfPos[each.rstrip()] = ErsteLinie.split(":").index(each)
                print(DictOfPos)

                FreeID = 1
                with open(ImportDatei, "r") as csvfile:
                    reader = csv.reader(csvfile, delimiter=":", quotechar="\"")
                    print("Lade preisliste")
                    DictList = []
                    for eachLine in reader:
                        if not "artikel" in eachLine or not "preisek" in eachLine:
                            if len(str(FreeID)) > 2:
                                if str(FreeID)[-3] + str(FreeID)[-2] + str(FreeID)[-1] == "000":
                                    print("Lade " + str(FreeID))
                            if str(FreeID)[-1] == "0":
                                #print("Lade " + str(FreeID))
                                #print("Geladene daten werden in die datenbank importiert")
                                #Artikel.insert_many(DictList).execute()
                                threading.Thread(target=SavePreisvorschlag, args=[DictList]).start()
                                DictList = []
                                    
                            Dict = {}
                            
                            while True:
                                query = Artikel.select().where(Artikel.identification == "P" + str(FreeID))
                                if not query.exists():
                                    break
                                FreeID = FreeID + 1

                            
                            for eachPos, eachName in enumerate(DictOfPos):
                                Dict[eachName] = eachLine[eachPos]

                            Dict["identification"] = "P" + str(FreeID)
                            
                            Dict["lieferant"] = LieferantName
                            Dict["preisek"] = Dict["preisek"].replace(",", ".")
                            Dict["preisvkh"] = Dict["preisvkh"].replace(",", ".")
                            Dict["preisvk"] = Dict["preisvk"].replace(",", ".")
                            
                            DictList.append(Dict)

                            FreeID = FreeID + 1
                            
                    print("Geladene daten werden in die datenbank importiert")
                    Artikel.insert_many(DictList).execute()

                BlueSave("LastChange", str(NewLastChange), ImportData)
                memory_db.close()

def GetBewegung(Dict):
    print("GetBewegung")
    id = str(Dict["identification"])
    local_db.connect()
    query = Bewegung.select().where(Bewegung.identification == id)
    if query.exists():
        object = Bewegung.get(Bewegung.identification == id)
        Antwort = model_to_dict(object)
    else:
        Antwort = {}
    local_db.close()
    return Antwort

def SearchArt(Dict):
    print("SearchArt")
    for key, var in Dict.items():
        print(str(key) + ": " + str(var))

    local_db.connect()
    if not Dict["suche"] == "":
        if Dict["suche"].isdigit():
            query = Artikel.select().where((Artikel.identification == str(Dict["suche"])) | (Artikel.barcode == str(Dict["suche"])) | (Artikel.artikel == str(Dict["suche"])) | (Artikel.artikel2 == str(Dict["suche"])) | (Artikel.artikel3 == str(Dict["suche"])) | (Artikel.artikel4 == str(Dict["suche"])))
        else:
            query = Artikel.select().where((Artikel.identification == str(Dict["suche"])) | (Artikel.artikel == str(Dict["suche"])) | (Artikel.artikel2 == str(Dict["suche"])) | (Artikel.artikel3 == str(Dict["suche"])) | (Artikel.artikel4 == str(Dict["suche"])))
        

    Antwort = []
    while True:
        Count = 1
        for ID in query:
            Antwort.append(str(ID.identification))
            if Count == INDEXLIMIT:
                break
            else:
                Count = Count + 1
        break
    local_db.close()
    return Antwort

def GetArt(Dict):
    print("GetArt")
    id = str(DATA["identification"])
    print("id: " + str(id))

    local_db.connect()
    query = Artikel.select().where(Artikel.identification == id)
    if query.exists():
        object = Artikel.get(Artikel.identification == id)
        Antwort = model_to_dict(object)
    else:
        Antwort = {}
    local_db.close()
    return Antwort

def SetArt(Dict):
    print("SetArt")
    id = str(DATA["identification"])
    print("id: " + str(id))
    try:
        local_db.connect()
        DATA["lastchange"] = str(Timestamp())
        ThisArtikel = dict_to_model(Artikel, DATA)
        ThisArtikel.save()
        local_db.close()
        Antwort = True
    except:
        Antwort = False
    return Antwort

def AddArt(Dict):
    global BeID
    print("AddArt")
    id = str(DATA["identification"])
    add = str(DATA["add"])
    del DATA["add"]
    print("add:" + str(add))
    local_db.connect()

    while True:
        query = Bewegung.select().where(Bewegung.identification == str(BeID))
        if not query.exists():
            break
        BeID = BeID + 1

    object = Artikel.get(Artikel.identification == id)
    object.lastchange = str(Timestamp())
    if "-" in add:
        add = int(add[1:])
        start = float(object.anzahl)
        object.anzahl = object.anzahl - add
        end = float(object.anzahl)
        if not object.anzahl < 0:
            object.save()
            object2 = Bewegung.create(identification=str(BeID),
                                      bcode=str(id),
                                      datum=str(Date()),
                                      start=start,
                                      end=end,
                                      preisek=object.preisek,
                                      preisvkh=object.preisvkh,
                                      preisvk=object.preisvk,
                                      mode="MISC",
                                      user=str(ipname[0]))
            object2.save()
    else:
        start = float(object.anzahl)
        object.anzahl = object.anzahl + int(add)
        end = float(object.anzahl)
        print("Anzahl " + str(object.anzahl))
        object.save()
        object2 = Bewegung.create(identification=str(BeID),
                                  bcode=str(id),
                                  datum=str(Date()),
                                  start=start,
                                  end=end,
                                  preisek=object.preisek,
                                  preisvkh=object.preisvkh,
                                  preisvk=object.preisvk,
                                  mode="MISC",
                                  user=str(ipname[0]))
        object2.save()
    Antwort = model_to_dict(object)
    local_db.close()
    BeID = BeID + 1
    return Antwort

def GetID():
    print("GetID")
    FreeID = 100000
    local_db.connect()
    while True:
        query = Artikel.select().where(Artikel.identification == str(FreeID))
        if not query.exists():
            break
        FreeID = FreeID + 1

    ThisArtikel = Artikel.create(creation=str(Date()),
                                 lastchange=str(Timestamp()),
                                 barcode=int(IDToBarcode(FreeID)),
                                 identification=str(FreeID))
    ThisArtikel.save()

    object = Artikel.get(Artikel.identification == str(FreeID))
    Antwort = model_to_dict(object)

    local_db.close()
    return Antwort

threading.Thread(target=Preisvorschlag).start()
#Preisvorschlag()

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
        DATA = json.loads(DATA)  # data loaded

        Debug("DATA : " + str(DATA))

        mode = DATA["mode"]
        print("mode: " + str(mode))

        del DATA["mode"]

        Antwort = "x"

        if mode == "GetBewegung":#return Dict of Bewegung
            Antwort = GetBewegung(DATA)

        if mode == "GetBewegungIndex":# return Int of aktual bewegung
            print("GetBewegungIndex")
            Antwort = int(BeID)

        if mode == "SearchArt":#return List of IDs
            Antwort = SearchArt(DATA)

        if mode == "GetArt":#return Dict
            Antwort = GetArt(DATA)

        if mode == "SetArt":#return Bool of sucess
            Antwort = SetArt(DATA)

        if mode == "AddArt":#return Dict
            Antwort = AddArt(DATA)

        if mode == "GetID":#return Dict
            Antwort = GetID()

        Debug("Sende : " + str(Antwort))
        Antwort = json.dumps(Antwort)  # data serialized
        Antwort = Antwort.encode()
        c.send(Antwort)
c.close()
