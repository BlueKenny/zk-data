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
#import base64

import threading

SERVER_PORT=10000

BYTE_LENGHT = 2048

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

if BlueLoad("Telegram", "DATA/DATA") == "1":
    Telegram = True
    try:
        from telethon import TelegramClient, utils
    except:
        import os
        print("Module Telethon, not installed, starting Installation...")
        os.system("pip3 install --user telethon")
        print("Module Telethon Installed, please restart APP...")
        
    api_id = 291651
    api_hash = '0f734eda64f8fa7dea8ed9558fd447e9'
    client = TelegramClient('telepygram', api_id, api_hash)
    isConnected = client.connect() # return True
    print("Connection: " + str(isConnected))
    isAuthorized = client.is_user_authorized()
    print("Authorized: " + str(isAuthorized))

    if not isAuthorized:
        phone_number = input("Enter your phone number\nIn international format please\n")
        print("Phone is " + str(phone_number))
        client.send_code_request(phone_number)
        authorized_code = input("Please enter code:\n")
        me = client.sign_in(phone_number, authorized_code)

    TelegramContact = BlueLoad("TelegramContact", "DATA/DATA")
    client.send_message(TelegramContact, "Server gestarted")
        
    Telegram = True

else:
    Telegram = False
    BlueSave("Telegram", "0", "DATA/DATA")
    BlueSave("TelegramContact", "", "DATA/DATA")

try: from peewee import *
except:
    if sys.platform == "linux": os.system("pip3 install --user peewee")

SERVER_SQL=BlueLoad("SERVERSQL", "DATA/DATA")
if SERVER_SQL == "None":
    SERVER_SQL = "127.0.0.1"
    SERVER_SQL=BlueSave("SERVERSQL", SERVER_SQL, "DATA/DATA")

from playhouse.migrate import *
from playhouse.shortcuts import model_to_dict, dict_to_model

local_db = SqliteDatabase("DATA/stock.db")
local_migrator = SqliteMigrator(local_db)

kunde_db = SqliteDatabase("DATA/kunde.db")
kunde_migrator = SqliteMigrator(kunde_db)

lieferschein_db = SqliteDatabase("DATA/lieferschein.db")
lieferschein_migrator = SqliteMigrator(lieferschein_db)

FreeID = 100000

class Lieferschein(Model):
    identification = CharField(primary_key = True)
    kunde_id = CharField(default="0")
    kunde_name = CharField(default="")
    datum = CharField(default=str(Date()))
    lastchange = CharField(default=str(Timestamp()))
    linien = CharField(default="")
    anzahl = CharField(default="")
    bcode = CharField(default="")
    name = CharField(default="")
    preis = CharField(default="")
    fertig = BooleanField(default=False)
    user = CharField(default = "")
    total = FloatField(default="0.0")

    class Meta:
        database = lieferschein_db

class Kunde(Model):
    identification = CharField(primary_key = True)
    name = CharField(default="")
    land = CharField(default="")
    adresse = CharField(default="")
    plz = IntegerField(default=0)
    ort = CharField(default="")
    email1 = CharField(default="")
    email2 = CharField(default="")
    email3 =CharField(default="")
    tel1 = IntegerField(default=0)
    tel2 = IntegerField(default=0)
    tel3 = IntegerField(default=0)
    tva = CharField(default="")
    credit = FloatField(default=0.0)
    debit = FloatField(default=0.0)
    solde_2015 = FloatField(default=0.0)
    solde_2016 = FloatField(default=0.0)
    solde_2017 = FloatField(default=0.0)
    solde_2018 = FloatField(default=0.0)
    sprache_de = BooleanField(default = False)
    sprache_fr = BooleanField(default = False)
    sprache_nl = BooleanField(default = False)
    lastchange = CharField(default=str(Timestamp()))
    creation = CharField(default=str(Date()))
    info = TextField(default="")

    class Meta:
        database = kunde_db

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
    groesse = CharField(default = "")

    class Meta:
        database = local_db


local_db.connect()

try: local_db.create_tables([Artikel])
except: print("Artikel table exists in local_db")

try: migrate(local_migrator.add_column("Artikel", "groesse", CharField(default = "")))
except: print("Artikel:groesse:existiert schon")

local_db.close()


kunde_db.connect()

try: kunde_db.create_tables([Kunde])
except: print("Kunde table exists in kunde_db")

try: migrate(kunde_migrator.add_column("Kunde", "land", CharField(default = "")))
except: print("Kunde:land:existiert schon")
try: migrate(kunde_migrator.add_column("Kunde", "info", TextField(default = "")))
except: print("Kunde:info:existiert schon")

kunde_db.close()



lieferschein_db.connect()

try: lieferschein_db.create_tables([Lieferschein])
except: print("Lieferschein table exists in lieferschein_db")

try: migrate(lieferschein_migrator.add_column("Lieferschein", "fertig", BooleanField(default=False)))
except: print("Lieferschein:fertig:existiert schon")
try: migrate(lieferschein_migrator.add_column("Lieferschein", "user", CharField(default="")))
except: print("Lieferschein:user:existiert schon")
try: migrate(lieferschein_migrator.add_column("Lieferschein", "total", FloatField(default=0.0)))
except: print("Lieferschein:total:existiert schon")
try: migrate(lieferschein_migrator.add_column("Lieferschein", "kunde_name", CharField(default="")))
except: print("Lieferschein:kunde_name:existiert schon")

lieferschein_db.close()


local_db.connect()
try:
    local_db.create_tables([Bewegung])
except:
    print("Bewegung table exists in local_db")
local_db.close()

# Ordner
DIR = ""
BlueMkDir(DIR + "DATA")
BlueMkDir(DIR + "Import")
BlueMkDir(DIR + "Import/Preise")

Barcodes = {}


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

# LOAD
print("LOAD DATAbase Stock")

SERVER_IP = ("", SERVER_PORT)
s = socket.socket()

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try: s.bind(SERVER_IP)
except: print("Server Port schon gebunden")
s.listen(50)


def KundenLaden():
    import csv
    with open('kd.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=':', quotechar='"')
        for row in sorted(spamreader):
            if not "identification" in row[0]:
                Dict = {}
                print(row)
                Dict["identification"] = str(row[0])
                Dict["name"] = row[1]
                Dict["adresse"] = row[2]
                Dict["plz"] = row[3]
                if "BG-" in Dict["plz"]:
                    Dict["land"] = "BG"
                    Dict["plz"] = Dict["plz"].replace("BG-", "")
                if "BE" in Dict["plz"]:
                    Dict["land"] = "BE"
                    Dict["plz"] = Dict["plz"].replace("BE", "")
                if "B " in Dict["plz"]:
                    Dict["land"] = "BE"
                    Dict["plz"] = Dict["plz"].replace("B ", "")
                if "B-" in Dict["plz"]:
                    Dict["land"] = "BE"
                    Dict["plz"] = Dict["plz"].replace("B-", "")
                if "L-" in Dict["plz"]:
                    Dict["land"] = "LU"
                    Dict["plz"] = Dict["plz"].replace("L-", "")
                try: Dict["plz"] = int(Dict["plz"])
                except: Dict["plz"] = 0
                Dict["ort"] = row[4].upper()
                Dict["email1"] = row[5].replace("-", "")
                Dict["email2"] = row[6].replace("-", "")
                Dict["email3"] = row[7].replace("-", "")
                try:
                    Dict["tel1"] = row[8].replace("/", "").replace(".", "").replace(" ", "").replace("tel", "")
                    Dict["tel1"] = int(Dict["tel1"])
                except: Dict["tel1"] = 0
                try:
                    Dict["tel2"] = row[9].replace("/", "").replace(".", "").replace(" ", "").replace("tel", "")
                    Dict["tel2"] = int(Dict["tel2"])
                except: Dict["tel2"] = 0
                try:
                    Dict["tel3"] = row[10].replace("/", "").replace(".", "").replace(" ", "").replace("tel", "")
                    Dict["tel3"] = int(Dict["tel3"])
                except: Dict["tel3"] = 0
                Dict["tva"] = row[11]
                Dict["solde_2015"] = row[12].replace(" ", "").replace("€", "").replace(".", "").replace("-", "").replace(",", ".")
                if Dict["solde_2015"] == "": Dict["solde_2015"] = 0
                Dict["solde_2016"] = row[13].replace(" ", "").replace("€", "").replace(".", "").replace("-", "").replace(",", ".")
                if Dict["solde_2016"] == "": Dict["solde_2016"] = 0
                Dict["solde_2017"] = row[14].replace(" ", "").replace("€", "").replace(".", "").replace("-", "").replace(",", ".")
                if Dict["solde_2017"] == "": Dict["solde_2017"] = 0
                

                kunde_db.connect()
                query = Kunde.select().where(Kunde.identification == Dict["identification"])
                if not query.exists():
                    ThisArtikel = Kunde.create(identification = Dict["identification"])
                    ThisArtikel.save()

                ThisArtikel = dict_to_model(Kunde, Dict)
                ThisArtikel.save()

                kunde_db.close()

#KundenLaden()

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
                local_db.connect()
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
                local_db.close()


def SearchKunden(Dict):# Give Dict with Search return List of IDs 
    print("SearchKunden")
    for key, var in Dict.items():
        print(str(key) + ": " + str(var))

    kunde_db.connect()

    if not Dict["identification"] == "":
        query = Kunde.select().where(Kunde.identification == Dict["identification"])
    else:
        query = Kunde.select()
    
    if not Dict["name"] == "":
        query2 = Kunde.select().where(Kunde.name.contains(Dict["name"]))
        #query2 = Kunde.select().where(Dict["name"] in Kunde.name)
    else:
        query2 = Kunde.select()
     
    Antwort = []
    while True:
        Count = 1
        for ID in query:
            if ID in query2:
                Antwort.append(str(ID.identification))
                if Count == INDEXLIMIT:
                    break
                else:
                    Count = Count + 1
        break
    kunde_db.close()
    return Antwort


def SearchArt(Dict):# Give Dict with Search return List of IDs 
    print("SearchArt")
    for key, var in Dict.items():
        print(str(key) + ": " + str(var))

    local_db.connect()
    Dict["suche"] = Dict["suche"].upper()
    
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

def SearchLieferschein(Dict):# Give Dict with Search return List of IDs 
    print("SearchLieferschein")
    for key, var in Dict.items():
        print(str(key) + ": " + str(var))

    lieferschein_db.connect()

    if not Dict["identification"] == "":
        query = Lieferschein.select().where(Lieferschein.identification == Dict["identification"])
        print("query selected")
    else:
        query = Lieferschein.select()
    
    if not Dict["kunde_id"] == "":
        query2 = Lieferschein.select().where(Lieferschein.kunde_id == Dict["kunde_id"])
        print("query2 selected")
    else:
        query2 = Lieferschein.select()

    if Dict["fertig"] == False:
        query3 = Lieferschein.select().where(Lieferschein.fertig == Dict["fertig"])
        print("query3 selected")
    else:
        query3 = Lieferschein.select()

    if Dict["eigene"] == True:
        query4 = Lieferschein.select().where(Lieferschein.user == str(ipname[0]))
        print("query4 selected")
    else:
        query4 = Lieferschein.select()
        
    Antwort = []
    while True:
        Count = 1
        for ID in query:
            print("Start test of " + ID.identification)
            if ID in query2 and ID in query3 and ID in query4:
                print("End test of " + ID.identification)
                Antwort.append(str(ID.identification))
                if Count == INDEXLIMIT:
                    break
                else:
                    Count = Count + 1
        print("End of IDs in query")
        break
    try: lieferschein_db.close()# Unfinalized things ?
    except: True    
    return Antwort

def NeuerLieferschein():# return Dict
    print("NeuerLieferschein")
    FreierLieferschein = 0
    lieferschein_db.connect()
    while True:
        query = Lieferschein.select().where(Lieferschein.identification == str(FreierLieferschein))
        if not query.exists():
            break
        FreierLieferschein = FreierLieferschein + 1

    ThisLieferschein = Lieferschein.create(linien="0", anzahl="1", bcode="", name="", preis="0.0", user=str(ipname[0]) ,identification=str(FreierLieferschein))
    ThisLieferschein.save()

    object = Lieferschein.get(Lieferschein.identification == str(FreierLieferschein))
    Antwort = model_to_dict(object)

    lieferschein_db.close()
    return Antwort

def GetLieferschein(Dict):# return Dict
    print("GetLieferschein")
    lieferschein_db.connect()

    lieferschein = str(Dict["identification"])
    query = Lieferschein.select().where(Lieferschein.identification == lieferschein)
    if query.exists():
        object = Lieferschein.get(Lieferschein.identification == lieferschein)
        Antwort = model_to_dict(object)
    else:
        Antwort = {}
    
    lieferschein_db.close()
    return Antwort

def SetLieferschein(Dict):# return Bool of sucess
    print("SetLieferschein")
    id = str(Dict["identification"])
    print("id: " + str(id))
    lieferschein_db.connect()
    if True:#try:
        Dict["lastchange"] = str(Timestamp())
        
        try: Dict["kunde_name"] = GetKunden({"identification":Dict["kunde_id"]})["name"]
        except: Dict["kunde_name"] = ""
        
        if Dict["linien"] == "":#wenn er leer ist
            Dict["linien"] = "0"
            Dict["anzahl"] = "1"
            Dict["bcode"] = ""
            Dict["name"] = ""
            Dict["preis"] = "0.0"
        if not Dict["bcode"].split("|")[-1] == "":# 1 Neue Linie Hinzufügen
            ActualSize = float(sys.getsizeof(json.dumps(Dict).encode()))
            MaxSize = BYTE_LENGHT * 0.8
            print("\nActualSize: " + str(ActualSize))
            print("MaxSize: " + str(MaxSize) + "\n")
            if ActualSize < MaxSize:        
                Dict["linien"] = Dict["linien"] + "|" + str(int(Dict["linien"].split("|")[-1]) + 1)
                Dict["anzahl"] = Dict["anzahl"] + "|1"
                Dict["bcode"] = Dict["bcode"] + "|"
                Dict["name"] = Dict["name"] + "|"
                Dict["preis"] = Dict["preis"] + "|0.0"
        # Linien zusammen setzen
        NeuerDict = Dict.copy()
        NeuerDict["linien"] = []
        NeuerDict["anzahl"] = []
        NeuerDict["bcode"] = []
        NeuerDict["name"] = []
        NeuerDict["preis"] = []
        for linie in Dict["linien"].split("|"):# für jede linie im Dict
            linie = int(linie)
            if Dict["bcode"].split("|")[linie] in NeuerDict["bcode"] and not len(Dict["bcode"].split("|")[linie]) < 3:# wenn schon im Neuen dict
                #print("Schon im Dict " + str(linie))
                NeuerDict["anzahl"][NeuerDict["bcode"].index(Dict["bcode"].split("|")[linie])] = str(int(NeuerDict["anzahl"][NeuerDict["bcode"].index(Dict["bcode"].split("|")[linie])]) + int(Dict["anzahl"].split("|")[linie]))
            else:
                #print("Noch nicht im Dict " + str(linie))
                try: NeuerDict["linien"].append(str(int(NeuerDict["linien"][-1]) + 1))
                except: NeuerDict["linien"].append("0")
                NeuerDict["anzahl"].append(str(Dict["anzahl"].split("|")[linie]))
                NeuerDict["bcode"].append(str(Dict["bcode"].split("|")[linie]))
                NeuerDict["name"].append(str(Dict["name"].split("|")[linie]))
                NeuerDict["preis"].append(str(Dict["preis"].split("|")[linie]))
        #print("NeuerDict " + str(NeuerDict))
        Dict["linien"] = "|".join(NeuerDict["linien"])
        Dict["anzahl"] = "|".join(NeuerDict["anzahl"])
        Dict["bcode"] = "|".join(NeuerDict["bcode"])
        Dict["name"] = "|".join(NeuerDict["name"])
        Dict["preis"] = "|".join(NeuerDict["preis"])

        query = Lieferschein.select().where(Lieferschein.identification == Dict["identification"])
        if query.exists():
            object = Lieferschein.get(Lieferschein.identification == Dict["identification"])
            AlterDict = model_to_dict(object)
        else:
            AlterDict = {}

        FertigeBcodes = []
        for NeuerBcode in Dict["bcode"].split("|"):
            if not NeuerBcode == "" and not NeuerBcode in FertigeBcodes:
                NeuePos = int(Dict["bcode"].split("|").index(NeuerBcode))
                NeueAnzahl = 0.0
                for eachLine in Dict["linien"].split("|"):
                    eachLine = int(eachLine)
                    if Dict["bcode"].split("|")[eachLine] == NeuerBcode:
                        NeueAnzahl = NeueAnzahl + float(Dict["anzahl"].split("|")[eachLine])
                AlteAnzahl = 0.0
                for eachLine in AlterDict["linien"].split("|"):
                    eachLine = int(eachLine)
                    if AlterDict["bcode"].split("|")[eachLine] == NeuerBcode:
                        AlteAnzahl = AlteAnzahl + float(AlterDict["anzahl"].split("|")[eachLine])
                DiffAnzahl = NeueAnzahl - AlteAnzahl
                FertigeBcodes.append(NeuerBcode)
                if not str(DiffAnzahl) == "0.0":
                    print(NeuerBcode + " " + str(DiffAnzahl))
                    if "-" in str(DiffAnzahl): DiffAnzahl = str(DiffAnzahl).replace("-", "")
                    else: DiffAnzahl = "-" + str(DiffAnzahl)
                    AddArt({"identification":str(NeuerBcode), "add":str(DiffAnzahl)})
                    
   
        for AlterBcode in AlterDict["bcode"].split("|"):
            if not AlterBcode in Dict["bcode"].split("|") and not AlterBcode in FertigeBcodes:
                NeueAnzahl = 0.0
                for eachLine in Dict["linien"].split("|"):
                    eachLine = int(eachLine)
                    if Dict["bcode"].split("|")[eachLine] == AlterBcode:
                        NeueAnzahl = NeueAnzahl + float(Dict["anzahl"].split("|")[eachLine])
                AlteAnzahl = 0.0
                for eachLine in AlterDict["linien"].split("|"):
                    eachLine = int(eachLine)
                    if AlterDict["bcode"].split("|")[eachLine] == AlterBcode:
                        AlteAnzahl = AlteAnzahl + float(AlterDict["anzahl"].split("|")[eachLine])
                DiffAnzahl = NeueAnzahl - AlteAnzahl
                FertigeBcodes.append(AlterBcode)
                if not str(DiffAnzahl) == "0.0":
                    print(NeuerBcode + " " + str(DiffAnzahl))
                    if "-" in str(DiffAnzahl): DiffAnzahl = str(DiffAnzahl).replace("-", "")
                    else: DiffAnzahl = "-" + str(DiffAnzahl)
                    AddArt({"identification":str(AlterBcode), "add":str(DiffAnzahl)})

        ThisArtikel = dict_to_model(Lieferschein, Dict)
        ThisArtikel.save()
        Antwort = True
    #except:
    #    Antwort = False
    
    lieferschein_db.close()
    return Antwort

def GetArt(Dict):# return Dict
    print("GetArt")
    try: local_db.connect()
    except: True

    try:
        bcode = str(Dict["identification"])
        query = Artikel.select().where(Artikel.identification == bcode)
        print("GetArt identification")
        if query.exists():
            object = Artikel.get(Artikel.identification == bcode)
            Antwort = model_to_dict(object)
        else:
            Antwort = {}
    except:
        barcode = int(Dict["barcode"])
        query = Artikel.select().where(Artikel.barcode == barcode)
        print("GetArt barcode")
        if query.exists():
            object = Artikel.get(Artikel.barcode == barcode)
            Antwort = model_to_dict(object)
        else:
            Antwort = {}

    
    local_db.close()
    return Antwort

def GetKunden(Dict):# return Dict
    print("GetKunden")
    kunde_db.connect()

    if True:#try:
        query = Kunde.select().where(Kunde.identification == str(Dict["identification"]))
        if query.exists():
            object = Kunde.get(Kunde.identification == str(Dict["identification"]))
            Antwort = model_to_dict(object)
        else:
            Antwort = {}
    #except:
    #    Antwort =  {}
    
    kunde_db.close()
    return Antwort


def SetArt(Dict):# return Bool of sucess
    print("SetArt")
    id = str(Dict["identification"])
    print("id: " + str(id))
    local_db.connect()
    try:
        Dict["lastchange"] = str(Timestamp())
        ThisArtikel = dict_to_model(Artikel, Dict)
        ThisArtikel.save()
        Antwort = True
    except:
        Antwort = False
    local_db.close()
    return Antwort

def AddArt(Dict):# return Bool of sucess
    global BeID
    print("AddArt")
    id = str(Dict["identification"])
    add = str(Dict["add"])
    del Dict["add"]
    print("add:" + str(add))
    local_db.connect()

    while True:
        query = Bewegung.select().where(Bewegung.identification == str(BeID))
        if not query.exists():
            break
        BeID = BeID + 1

    try: object = Artikel.get(Artikel.identification == id)
    except: return False
    object.lastchange = str(Timestamp())
    
    start = float(object.anzahl)
    if "-" in add:
        add = float(add[1:])
        StartErgebnis = object.anzahl
        Anzahl = float(add)
        object.anzahl = object.anzahl - float(add)
        EndErgebnis = object.anzahl
        
        if not object.minimum == 0.0:
            if StartErgebnis < object.minimum:
                ZuBestellen = Anzahl
            else:
                ZuBestellen = object.minimum - EndErgebnis
            if ZuBestellen > 0:        
                ZuBestellenLinie = str(ZuBestellen) + "x  [" + object.name_de + "] Rest : " + str(object.anzahl) + " [" + object.identification + "] Lieferant : " + object.lieferant + " Artikel : " + object.artikel + "\n"
                open("DATA/MINIMUM", "a").write(str(ZuBestellenLinie))
                client.send_message(TelegramContact, ZuBestellenLinie)    
    else:
        object.anzahl = object.anzahl + float(add)
        
    print("Anzahl " + str(object.anzahl))
    
    if object.anzahl < 0:
        Antwort = False
    else:
        object.save()
        end = float(object.anzahl)
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
        BeID = BeID + 1
        Antwort = True
    
    local_db.close()
    return Antwort

def GetGewinn(Dict): #return Float
    print("GetGewinn")
    
    try: local_db.connect()
    except: True
    query = Bewegung.select().where(Bewegung.datum == str(Dict["datum"]))
    local_db.close()
    Summe = 0.0
    for Each in query:
        Anzahl = Each.start - Each.end
        Summe = Summe + ((Each.preisvkh - Each.preisek) * Anzahl)
    
    return Summe
    
def GetID():# return Dict
    global FreeID
    print("GetID")
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

def GetBarcode(Position, Bytes, User): # return String
    global Barcodes
    #print("Position: " + str(Position))
    #print("Bytes: " + str(Bytes))
    #print("User: " + str(User))
    if Position == 0:
        Barcodes[User] = {}
    Barcodes[User][Position] = base64.b64decode(Bytes) #Bytes.encode()
    #print(Barcodes[User])

    ReadData = b""
    for key, item in Barcodes[User].items():
        #print("item: " + str(item))
        ReadData = ReadData + item
    
    #image = open("barcode.jpg", "wb").write(ReadData)

    #os.system("zbarimg barcode.jpg")
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
        DATA = c.recv(BYTE_LENGHT)
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

        if mode == "SearchKunden":#return List of IDs
            Antwort = SearchKunden(DATA)

        if mode == "SearchArt":#return List of IDs
            Antwort = SearchArt(DATA)

        if mode == "NeuerLieferschein":#return Dict
            Antwort = NeuerLieferschein()

        if mode == "SearchLieferschein":#return List of IDs
            Antwort = SearchLieferschein(DATA)

        if mode == "GetArt":#return Dict
            Antwort = GetArt(DATA)

        if mode == "GetLieferschein":#return Dict
            Antwort = GetLieferschein(DATA)

        if mode == "GetKunden":#return Dict
            Antwort = GetKunden(DATA)

        if mode == "SetArt":#return Bool of sucess
            Antwort = SetArt(DATA)

        if mode == "SetLieferschein":#return Bool of sucess
            Antwort = SetLieferschein(DATA)

        if mode == "AddArt":#return Dict
            Antwort = AddArt(DATA)

        if mode == "GetID":#return Dict
            Antwort = GetID()

        if mode == "GetBarcode":#return String
            Antwort = GetBarcode(DATA["position"], DATA["bytes"], ipname[0])
        
        if mode == "GetGewinn": # return Float
            Antwort = GetGewinn(DATA)

        Debug("Sende : " + str(Antwort))
        Antwort = json.dumps(Antwort)  # data serialized
        Antwort = Antwort.encode()
        c.send(Antwort)
c.close()
