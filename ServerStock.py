#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
from libs.debug import *
from libs.BlueFunc import *
import os
from libs.RoundUp import * 
import datetime
import time
from libs.barcode import *
import json

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


from peewee import *
SERVER_SQL=BlueLoad("SERVERSQL", "DATA/DATA")
if SERVER_SQL == "None":
    SERVER_SQL = "127.0.0.1"
    SERVER_SQL=BlueSave("SERVERSQL", SERVER_SQL, "DATA/DATA")

local_db = SqliteDatabase("DATA/stock.db")
#memory_db = SqliteDatabase(":memory:")
#local_db = MySQLDatabase('web', user='root', password='', host=SERVER_SQL, port=3306)
#extern_db= MySQLDatabase('web', user='root', password='', host='192.168.188.24', port=3306)#192.168.188.24

class Artikel(Model):# All Str are upper()
    identification = CharField(primary_key = True)
    name = CharField(null = True)
    artikel = CharField(null = True)
    artikel2 = CharField(null = True)
    artikel3 = CharField(null = True)
    artikel4 = CharField(null = True)
    barcode = IntegerField(null = True)
    lieferant = CharField(null = True)
    preisek = FloatField(null = True)
    preisvkh = FloatField(null = True)
    preisvk = FloatField(null = True)
    anzahl = FloatField(null = True)
    ort = CharField(null = True)
    lastchange = CharField(null = True)
    creation = CharField(null = True)
    minimum = FloatField(null = True)

    class Meta:
        database = local_db


local_db.connect()
try:
    local_db.create_tables([Artikel])
except:
    print("Artikel table exists in local_db")
local_db.close()

#extern_db.connect()
#try: extern_db.create_tables([ArtikelExtern])
#except: print("ArtikelExtern table exists")
#extern_db.close()

# Ordner
DIR = ""
BlueMkDir(DIR + "StockBewegung")
BlueMkDir(DIR + "DATA")

try:
    INDEXLIMIT = int(BlueLoad("IndexLimit", DIR + "DATA/DATA"))
except:
    INDEXLIMIT = 100
    BlueSave("IndexLimit", "100", DIR + "DATA/DATA")

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
                                                 name=StockNameList[eachFile],
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

# LOAD
print("LOAD DATAbase Stock") 
StockArtikelAnzahl = 0

print("StockArtikelAnzahl : " + str(StockArtikelAnzahl))

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

        #data_string = json.dumps(data)  # data serialized
        #data_loaded = json.loads(data)  # data loaded

        mode = DATA["mode"]
        print("mode: " + str(mode))

        del DATA["mode"]

        Antwort = "x"

        if mode == "SearchArt":#return List of IDs
            print("SearchArt")
            for key, var in DATA.items():
                print(str(key) + ": " + str(var))

            local_db.connect()
            query = Artikel.select().where((Artikel.identification == str(DATA["suche"])) |
                                           (Artikel.artikel == str(DATA["suche"])) |
                                           (Artikel.artikel2 == str(DATA["suche"])) |
                                           (Artikel.artikel3 == str(DATA["suche"])) |
                                           (Artikel.artikel4 == str(DATA["suche"])))
            Antwort = {}
            for ID in query:
                Antwort[ID.identification]=ID.lastchange
            local_db.close()

        if mode == "GetArt":#return Dict
            print("GetArt")
            id = str(DATA["identification"])
            print("id: " + str(id))


            local_db.connect()
            query = Artikel.select().where(Artikel.identification == id)
            if query.exists():
                object = Artikel.get(Artikel.identification == id)
                Antwort = {}
                Antwort["creation"] = object.creation
                Antwort["lastchange"] = object.lastchange
                Antwort["barcode"] = object.barcode
                Antwort["artikel"] = object.artikel
                Antwort["artikel2"] = object.artikel2
                Antwort["artikel3"] = object.artikel3
                Antwort["artikel4"] = object.artikel4
                Antwort["lieferant"] = object.lieferant
                Antwort["name"] = object.name
                Antwort["ort"] = object.ort
                Antwort["preisek"] = object.preisek
                Antwort["preisvkh"] = object.preisvkh
                Antwort["preisvk"] = object.preisvk
                Antwort["anzahl"] = object.anzahl
                Antwort["minimum"] = object.minimum
                Antwort["identification"] = object.identification
            else:
                Antwort = {}
                #Antwort["creation"] = ""
                #Antwort["lastchange"] = ""
                #Antwort["barcode"] = 0
                #Antwort["artikel"] = ""
                #Antwort["artikel2"] = ""
                #Antwort["artikel3"] = ""
                #Antwort["artikel4"] = ""
                #Antwort["lieferant"] = ""
                #Antwort["name"] = ""
                #Antwort["ort"] = ""
                #Antwort["preisek"] = 0.0
                #Antwort["preisvkh"] = 0.0
                #Antwort["preisvk"] = 0.0
                #Antwort["anzahl"] = 0.0
                #Antwort["minimum"] = 0.0
                #Antwort["identification"] = id

            local_db.close()

        if mode == "SetArt":
            Debug("Mode : " + mode)
            ID = int(DATA.split("(zKz)")[1].split("(zkz)")[0])
            Dict = {}
            Vars = DATA.split("(zKz)")[1].split("(zkz)")[1].split("|")
            for each in Vars:
                Dict[each.split("&zKz&")[0]] = each.split("&zKz&")[0]

            BlueMkDir(DIR + "Stock/" + str(ID)[-2] + str(ID)[-1])
            File = DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID)

            query = Artikel.select().where(Artikel.identification == str(ID))
            if not query.exists():
                ThisArtikel = Artikel.create(creation=str(Date()), identification=ID)
                ThisArtikel.save()

            if not ID in StockIDList:
                StockArtikelAnzahl = StockArtikelAnzahl  + 1 # Neuer Artikel
                BlueSave("Creation", str(Date()), File)
                StockCreationList[ID] = str(Date())
                StockIDList.append(ID)


            identification = CharField(primary_key=True)
            name = CharField(null=True)
            artikel = CharField(null=True)
            artikel2 = CharField(null=True)
            artikel3 = CharField(null=True)
            barcode = IntegerField(null=True)
            lieferant = CharField(null=True)
            preisek = FloatField(null=True)
            preisvkh = FloatField(null=True)
            preisvk = FloatField(null=True)
            anzahl = FloatField(null=True)
            ort = CharField(null=True)
            lastchange = CharField(null=True)
            creation = CharField(null=True)
            minimum = FloatField(null=True)

        if mode == "GetStockZahl":
            Debug("Mode : " + mode)
            Antwort = str(StockArtikelAnzahl)

        if mode == "ChangeStock":
            Debug("Mode : " + mode)
            BcodeSuche = int(DATA.split("(zKz)")[1].split("(zkz)")[0])
            Debug("BcodeSuche : " + str(BcodeSuche))
            NewStock = DATA.split("(zKz)")[1].split("(zkz)")[1]
            Debug("NewStock : " + NewStock)
            AltStock = str(StockAnzahlList[BcodeSuche])
            Debug("AltStock : " + AltStock )
            StockAnzahlList[BcodeSuche] = float(AltStock) + float(NewStock)
            BlueSave("Anzahl", str(StockAnzahlList[BcodeSuche]), "Stock/" + str(BcodeSuche)[-2] + str(BcodeSuche)[-1] + "/" + str(BcodeSuche))

            query = Artikel.select().where(Artikel.identification == str(BcodeSuche))
            if not query.exists():
                ThisArtikel = Artikel.create(creation=str(Date()), identification=str(BcodeSuche))
                ThisArtikel.save()
            ThisArtikel = Artikel(anzahl=StockAnzahlList[BcodeSuche], identification=str(BcodeSuche))
            ThisArtikel.save()

            BlueSave("LastChange", str(Date()), DIR + "Stock/" + str(BcodeSuche)[-2] + str(BcodeSuche)[-1] + "/" + str(BcodeSuche))
            StockLastChangeList[BcodeSuche] = str(Timestamp())

            BlueMkDir(DIR + "StockBewegung/" + str(Date()).split("-")[0])
            BlueMkDir(DIR + "StockBewegung/" + str(Date()).split("-")[0] + "/" + str(Date()).split("-")[1])
            DateiStockBewegung = DIR + "StockBewegung/" + str(Date()).split("-")[0] + "/" + str(Date()).split("-")[1] + "/" + str(Date()).split("-")[2] + ".csv"
            if not os.path.exists(DateiStockBewegung): open(DateiStockBewegung, "a").write("ID:QUANTITY FROM:QUANTITY TO:COST:PRICE VAT INCL.:PRICE VAT EXCL.:MODE:USER\n")
            open(DateiStockBewegung, "a").write(str(BcodeSuche) + ":" + str(AltStock) + ":" + str(StockAnzahlList[BcodeSuche]) + ":" + str(StockPreisEKList[BcodeSuche]) + ":" + str(StockPreisVKHList[BcodeSuche]) + ":" + str(StockPreisVKList[BcodeSuche]) + ":MISC:" + str(ipname[0]) + "\n")

        if mode == "SucheStock":
            Debug("Mode : " + mode)
            SucheSuche = str(DATA.split("(zKz)")[1].split("(zkz)")[0])
            SucheSuche = SucheSuche.upper()
            Debug("SucheSuche : " + SucheSuche)
            OrtSuche = DATA.split("(zKz)")[1].split("(zkz)")[1]
            OrtSuche = OrtSuche.upper()
            Debug("OrtSuche : " + OrtSuche)
            LieferantSuche = DATA.split("(zKz)")[1].split("(zkz)")[2]
            LieferantSuche = LieferantSuche.upper()
            Debug("LieferantSuche : " + LieferantSuche)

            indices = []
            #	ID		only 1 is possible
            if len(SucheSuche) == 6:
                try:
                    if int(SucheSuche) in StockIDList:
                        indices.append(int(SucheSuche))
                except: Debug("Search is not an ID")

            #	Barcode		only 1 is possible but for the moment multiple
            if len(SucheSuche) == 13:# Only Barcodes with 13 integers
                try:
                    int(SucheSuche)
                    isInt = True
                except:
                    isInt = False

                if isInt:
                    Debug("Test if Search is Barcode")
                    #ID = find_key_dict(StockBarcodeList, int(SucheSuche))
                    #if not ID in indices: indices.append(ID)
                    ListOfBarcodes = find_keys_dict(StockBarcodeList, int(SucheSuche))
                    if not ListOfBarcodes == None:
                        for ID in ListOfBarcodes:
                            if not ID in indices: indices.append(ID)
                else: Debug("len 13 but not an Int")
            #	Article		multiple choice possible
            ListOfArticles = find_keys_dict(StockArtikelList, str(SucheSuche))
            if not ListOfArticles == None:
                for ID in ListOfArticles:
                    if not ID in indices: indices.append(ID)
            #	Article2		multiple choice possible
            ListOfArticles = find_keys_dict(StockArtikel2List, str(SucheSuche))
            if not ListOfArticles == None:
                for ID in ListOfArticles:
                    if not ID in indices: indices.append(ID)
            #	Article3		multiple choice possible
            ListOfArticles = find_keys_dict(StockArtikel3List, str(SucheSuche))
            if not ListOfArticles == None:
                for ID in ListOfArticles:
                    if not ID in indices: indices.append(ID)
            #	Location		multiple choice possible
            if not OrtSuche == "":
                indices2 = indices;
                indices = []
                for ID in indices2:
                    if StockOrtList[ID] == str(OrtSuche):
                        indices.append(ID)

            #	Supplier		multiple choice possible
            if not LieferantSuche == "":
            #    indices2 = indices
            #    indices = []
            #    ListOfSupplier = find_keys_dict(StockLieferantList, str(LieferantSuche))
            #    if not ListOfSupplier == None:
            #        for ID in ListOfSupplier:
            #            if ID in indices2: indices.append(ID)
                indices2 = indices; indices = []
                for ID in indices2:
                    if StockLieferantList[ID] == str(LieferantSuche):
                        indices.append(ID)

            indices = indices[:INDEXLIMIT]
            if indices == []: indices = [0]

            try:
                Antwort = ""
                for eachDat in indices:
                    if Antwort == "":
                        Antwort = str(eachDat) + "|" + str(StockLastChangeList[eachDat])
                    else:
                        Antwort = Antwort + "<K>" + str(eachDat) + "|" + str(StockLastChangeList[eachDat])

            except:
                if Antwort == "": Antwort = "|"
                Debug("Nichts gefunden")

        if mode == "SearchStock":
            Debug("Mode : " + mode)
            SucheSuche = str(DATA.split("(zKz)")[1].split("(zkz)")[0])
            SucheSuche = SucheSuche.upper()
            Debug("SucheSuche : " + SucheSuche)
            OrtSuche = DATA.split("(zKz)")[1].split("(zkz)")[1]
            OrtSuche = OrtSuche.upper()
            Debug("OrtSuche : " + OrtSuche)
            LieferantSuche = DATA.split("(zKz)")[1].split("(zkz)")[2]
            LieferantSuche = LieferantSuche.upper()
            Debug("LieferantSuche : " + LieferantSuche)

            indices = []
            #	ID		only 1 is possible
            if len(SucheSuche) == 6:
                try:
                    if int(SucheSuche) in StockIDList:
                        indices.append(int(SucheSuche))
                except: Debug("Search is not an ID")

            #	Barcode		only 1 is possible but for the moment multiple
            if len(SucheSuche) == 13:# Only Barcodes with 13 integers
                try:
                    int(SucheSuche)
                    isInt = True
                except:
                    isInt = False

                if isInt:
                    Debug("Test if Search is Barcode")
                    #ID = find_key_dict(StockBarcodeList, int(SucheSuche))
                    #if not ID in indices: indices.append(ID)
                    ListOfBarcodes = find_keys_dict(StockBarcodeList, int(SucheSuche))
                    if not ListOfBarcodes == None:
                        for ID in ListOfBarcodes:
                            if not ID in indices: indices.append(ID)
                else: Debug("len 13 but not an Int")
            #	Article		multiple choice possible
            ListOfArticles = find_keys_dict(StockArtikelList, str(SucheSuche))
            if not ListOfArticles == None:
                for ID in ListOfArticles:
                    if not ID in indices: indices.append(ID)
            #	Article2		multiple choice possible
            ListOfArticles = find_keys_dict(StockArtikel2List, str(SucheSuche))
            if not ListOfArticles == None:
                for ID in ListOfArticles:
                    if not ID in indices: indices.append(ID)
            #	Article3		multiple choice possible
            ListOfArticles = find_keys_dict(StockArtikel3List, str(SucheSuche))
            if not ListOfArticles == None:
                for ID in ListOfArticles:
                    if not ID in indices: indices.append(ID)
            #	Location		multiple choice possible
            if not OrtSuche == "":
                indices2 = indices;
                indices = []
                for ID in indices2:
                    if StockOrtList[ID] == str(OrtSuche):
                        indices.append(ID)

            #	Supplier		multiple choice possible
            if not LieferantSuche == "":
            #    indices2 = indices
            #    indices = []
            #    ListOfSupplier = find_keys_dict(StockLieferantList, str(LieferantSuche))
            #    if not ListOfSupplier == None:
            #        for ID in ListOfSupplier:
            #            if ID in indices2: indices.append(ID)
                indices2 = indices; indices = []
                for ID in indices2:
                    if StockLieferantList[ID] == str(LieferantSuche):
                        indices.append(ID)

            indices = indices[:INDEXLIMIT]
            if indices == []: indices = [0]

            try:
                Antwort = " "
                for eachDat in indices:
                    Antwort = Antwort.rstrip() + str(eachDat) + "<K>"

            except: Debug("Nichts gefunden")


        Debug("Sende : " + str(Antwort))
        Antwort = json.dumps(Antwort)  # data serialized
        Antwort = Antwort.encode()
        c.send(Antwort)
c.close()
