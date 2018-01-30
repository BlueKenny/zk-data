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

SERVER_PORT=10000


from peewee import *
local_db = MySQLDatabase('web', user='root', password='', host='10.0.0.16', port=3306)
extern_db= MySQLDatabase('web', user='root', password='', host='192.168.188.24', port=3306)#192.168.188.24

class Artikel(Model):
    identification = CharField(primary_key = True)
    name = CharField(null = False)
    artikel = CharField(null = False)
    artikel2 = CharField(null = True)
    artikel3 = CharField(null = True)
    barcode = IntegerField(null = False)
    lieferant = CharField(null = False)
    preisek = FloatField(null = False)
    preisvkh = FloatField(null = False)
    preisvk = FloatField(null = False)
    anzahl = FloatField(null = False)
    lastchange = CharField(null = False)
    creation = CharField(null = False)

    class Meta:
        database = local_db  # this model uses the "people.db" database

class ArtikelExtern(Model):
    identification = CharField(primary_key = True)
    name = CharField(null = False)
    artikel = CharField(null = False)
    artikel2 = CharField(null = True)
    artikel3 = CharField(null = True)
    lieferant = CharField(null = False)
    preisvk = FloatField(null = False)
    anzahl = FloatField(null = False)
    lastchange = CharField(null = False)
    creation = CharField(null = False)

    class Meta:
        database = extern_db  # this model uses the "people.db" database


local_db.connect()
try: local_db.create_tables([Artikel])
except: print("Artikel table exists")
local_db.close()

#extern_db.connect()
#try: extern_db.create_tables([ArtikelExtern])
#except: print("ArtikelExtern table exists")
#extern_db.close()



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

def StockInventar():
    DateiName = "DATA/Inventur.csv"
    if os.path.exists(DateiName): os.remove(DateiName)
    Datei = open(DateiName, "a")

    Datei.write("ID:DESCRIPTION:QUANTITY:PRICE:TOTAL:" + Date() + "\n")
    TOTAL_END = 0.00
    for ID in StockIDList:
        ID = str(ID)
        DESCRIPTION = str(find_value_dict(StockNameList, int(ID))).replace(":", "")
        QUANTITY = str(find_value_dict(StockAnzahlList, int(ID)))
        PRICE = str(find_value_dict(StockPreisEKList, int(ID)))
        try: TOTAL = str(RoundUp0000(float(QUANTITY) * float(PRICE)))
        except: TOTAL = "0.00"
        TOTAL_END = TOTAL_END + float(TOTAL)

        PRICE = PRICE.replace(".", ",")# Show better in LibreOffice :)
        TOTAL = TOTAL.replace(".", ",")

        try:
            if not QUANTITY == "0":
                Datei.write(ID + ":" + DESCRIPTION + ":" + QUANTITY + ":" + PRICE + ":" + TOTAL + "\n")
        except: True

    Datei.write(":::TOTAL:" + str(RoundUp0000(TOTAL_END)).replace(".", ",") + "\n")

# Ordner
DIR = ""
BlueMkDir(DIR + "Stock")
BlueMkDir(DIR + "StockBewegung")
BlueMkDir(DIR + "Arbeiter")
BlueMkDir(DIR + "DATA")


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

StockIDList = []
ListeDerLieferanten = []
ArbeiterListe = []
BlockedIDList= []

try:
    INDEXLIMIT = int(BlueLoad("IndexLimit", DIR + "DATA/DATA"))
except:
    INDEXLIMIT = 20
    BlueSave("IndexLimit", "20", DIR + "DATA/DATA")


# LOAD
print("LOAD DATAbase Stock") 
StockArtikelAnzahl = 0
KundenAnzahl = 0
NeueKundenID = 10

for eachDir in os.listdir(DIR + "Stock/"):
    for eachFile in os.listdir(DIR + "Stock/" + eachDir):
        if True:#try:
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

            #try: StockPreisEKList[eachFile]=RoundUp0000(str(BlueLoad("PreisEK", datei)).replace(",", "."))
            #except: StockPreisEKList[eachFile] = "x"
            #try: StockPreisVKHList[eachFile]=RoundUp0000(str(BlueLoad("PreisVKH", datei)).replace(",", "."))
            #except: StockPreisVKHList[eachFile] = "x"
            #try: StockPreisVKList[eachFile]=RoundUp0000(str(BlueLoad("PreisVK", datei)).replace(",", "."))
            #except: StockPreisVKList[eachFile] = "x"

            #	Quantity
            ArticleQuantity = str(BlueLoad("Anzahl", datei))
            if ArticleQuantity == None or ArticleQuantity == "None" or ArticleQuantity == "x" or ArticleQuantity == "":
                ArticleQuantity = 0
                BlueSave("Anzahl", ArticleQuantity, datei)
            StockAnzahlList[eachFile]=int(ArticleQuantity)

            StockArtikelAnzahl = StockArtikelAnzahl  + 1
            if not StockLieferantList[eachFile] in ListeDerLieferanten: ListeDerLieferanten.append(StockLieferantList[eachFile])

            #ThisArtikel = Artikel.create(artikel=StockArtikelList[eachFile], name=StockNameList[eachFile], identification=eachFile)
            #ThisArtikel.save()
        #except: Debug("Failed to load")


for Arbeiter in os.listdir(DIR + "Arbeiter"):
    ArbeiterListe.append(Arbeiter)
if len(ArbeiterListe) == 0: ArbeiterListe.append("Arbeiter1")

print("StockArtikelAnzahl : " + str(StockArtikelAnzahl))
print("ListeDerLieferanten : " + str(ListeDerLieferanten))
print("KundenAnzahl : " + str(KundenAnzahl))
print("NeueKundenID : " + str(NeueKundenID))

StockInventar()

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

            query = Artikel.select().where(Artikel.identification == str(ID))
            if not query.exists():
                ThisArtikel = Artikel.create(creation=str(Date()), identification=ID)
                ThisArtikel.save()

            BlueSave("LastChange", str(Timestamp()), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
            StockLastChangeList[ID] = str(Timestamp())
            ThisArtikel = Artikel(lastchange=StockLastChangeList[ID], identification=ID)
            ThisArtikel.save()

            if not ID in StockIDList:
                StockArtikelAnzahl = StockArtikelAnzahl  + 1 # Neuer Artikel
                BlueSave("Creation", str(Date()), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                StockCreationList[ID] = str(Date())
                StockIDList.append(ID)

            if VarName == "Barcode":
                StockBarcodeList[ID]=str(Var)
                BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                ThisArtikel = Artikel(barcode=StockBarcodeList[ID], identification=ID)
                ThisArtikel.save()
            if VarName == "Artikel":
                StockArtikelList[ID]=str(Var).upper()
                BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                ThisArtikel = Artikel(artikel=StockArtikelList[ID], identification=ID)
                ThisArtikel.save()
            if VarName == "Artikel2":
                StockArtikel2List[ID]=str(Var).upper()
                BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                ThisArtikel = Artikel(artikel2=StockArtikel2List[ID], identification=ID)
                ThisArtikel.save()
            if VarName == "Artikel3":
                StockArtikel3List[ID]=str(Var).upper()
                BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                ThisArtikel = Artikel(artikel3=StockArtikel3List[ID], identification=ID)
                ThisArtikel.save()
            if VarName == "Lieferant":
                StockLieferantList[ID]=str(Var).upper()
                BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                if not StockLieferantList[ID] in ListeDerLieferanten: ListeDerLieferanten.append(StockLieferantList[ID]) # Neuer Artikel
                ThisArtikel = Artikel(lieferant=StockLieferantList[ID], identification=ID)
                ThisArtikel.save()
            if VarName == "Name":
                StockNameList[ID]=str(Var)
                BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                ThisArtikel = Artikel(name=StockNameList[ID], identification=ID)
                ThisArtikel.save()
            if VarName == "Ort":
                StockOrtList[ID]=str(Var).upper()
                BlueSave(str(VarName), str(Var).upper(), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                ThisArtikel = Artikel(lastchange=StockOrtList[ID], identification=ID)
                ThisArtikel.save()
            if VarName == "PreisEK":
                StockPreisEKList[ID]=str(Var)
                BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                ThisArtikel = Artikel(preisek=StockPreisEKList[ID], identification=ID)
                ThisArtikel.save()
            if VarName == "PreisVKH":
                StockPreisVKHList[ID]=str(Var)
                BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                ThisArtikel = Artikel(preisvkh=StockPreisVKHList[ID], identification=ID)
                ThisArtikel.save()
            if VarName == "PreisVK":
                StockPreisVKList[ID]=str(Var)
                BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                ThisArtikel = Artikel(preisvk=StockPreisVKList[ID], identification=ID)
                ThisArtikel.save()
            if VarName == "Anzahl":
                StockAnzahlList[ID]=str(Var)
                BlueSave(str(VarName), str(Var), DIR + "Stock/" + str(ID)[-2] + str(ID)[-1] + "/" + str(ID))
                ThisArtikel = Artikel(anzahl=StockAnzahlList[ID], identification=ID)
                ThisArtikel.save()

        if mode == "GetArtInfo":
            Debug("Mode : " + mode)
            print(DATA.split("(zKz)")[1])
            ID = DATA.split("(zKz)")[1].split("(zkz)")[0]
            Vars = str(DATA.split(str(ID))[1]).split("(zkz)")
            Debug("ID :  " + str(ID))
            Debug("Vars :  " + str(Vars))

            Antwort = str(ID)


            ID = int(ID)
            for Var in Vars:
                try:
                    if Var == "Artikel":  Antwort = Antwort + " | " + str(StockArtikelList[ID])
                    if Var == "Artikel2":  Antwort = Antwort + " | " + str(StockArtikel2List[ID])
                    if Var == "Artikel3":  Antwort = Antwort + " | " + str(StockArtikel3List[ID])
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

            #	Barcode		only 1 is possible
            if len(SucheSuche) == 13:# Only Barcodes with 13 integers
                if True:
                    ID = find_key_dict(StockBarcodeList, int(SucheSuche))
                    if not ID in indices: indices.append(ID)
                #except: Debug("Search is not a Barcode")
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
        Antwort = Antwort.encode()
        c.send(Antwort)
c.close()
